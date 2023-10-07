import argparse

import boto3
import datasets
from datasets import Dataset
from datasets.table import embed_table_storage
import re
import random
import json
import os

from database.entities.post import PostEntity
from database.tag_normalizer.util import load_normalizer_from_database
from database.utils.db_utils import connect_to_db
from database.utils.enums import numeric_categories
from dataset.utils.balance import balance_selections
from dataset.utils.format import format_posts_for_dataset
from dataset.utils.prune import prune_and_filter_tags
from utils.progress import Progress
from utils.load_yaml import load_yaml
from dataset.utils.selection_source import SelectionSource


def get_args():
    parser = argparse.ArgumentParser(prog='Build', description='Build an image dataset from JSONL file(s)')
    parser.add_argument('-o', '--output', metavar='PATH', type=str, help='Path where the dataset will be stored', required=True)
    parser.add_argument('-s', '--samples', metavar='FILE', type=str, action='append', help='Post JSONL file(s) to import', required=True)
    parser.add_argument('-a', '--agent', metavar='AGENT', type=str, help='Unique user agent string (e.g. "mycrawler/1.0 (by myusername)")', required=True)
    parser.add_argument('--export-tags', metavar='FILE', type=str, help='Export tag counts as a JSON file', required=False, default=None)
    parser.add_argument('--export-autocomplete', metavar='FILE', type=str, help='Export autocomplete hints as a a1111-sd-webui-tagcomplete CSV file', required=False, default=None)
    parser.add_argument('--min-posts-per-tag', metavar='COUNT', type=int, help='Minimum number of posts a tag must appear in to be included', required=False, default=100)
    parser.add_argument('--min-tags-per-post', metavar='COUNT', type=int, help='Minimum number of tags in a post for the post to be included (counted after min-posts-per-tag limit has been applied)', required=False, default=10)
    parser.add_argument('--prefilter', metavar='FILE', type=str, help='Prefilter YAML file', required=False, default='../examples/dataset/prefilter.yaml')
    parser.add_argument('--image-width', metavar='PIXELS', type=int, help='Maximum width for stored images', required=False, default=4096)
    parser.add_argument('--image-height', metavar='PIXELS', type=int, help='Maximum height for stored images', required=False, default=4096)
    parser.add_argument('--image-format', metavar='FORMAT', type=str, help='Storage image format [jpg, png]', choices=['jpg', 'png'], required=False, default='jpg')
    parser.add_argument('--image-quality', metavar='PERCENTAGE', type=int, help='Storage image quality (JPEG only)', required=False, default=85)
    parser.add_argument('--num-proc', metavar='COUNT', type=int, help='Maximum number of parallel processes', required=False, default=1)
    parser.add_argument('--upload-to-hf', metavar='USER_NAME/DATASET_NAME', type=int, help='Upload dataset to Huggingface (e.g. myuser/mynewdataset)', required=False, default=None)
    parser.add_argument('--upload-to-s3', metavar='S3_URL', type=int, help='Upload dataset to S3 (e.g. s3://some-bucket/some-path)', required=False, default=None)
    parser.add_argument('--limit', metavar='COUNT', type=int, help='Limit samples in dataset', required=False, default=None)
    parser.add_argument('--separator', metavar='STRING', type=str, help='Separator string for tag lists', required=False, default=' ')

    args = parser.parse_args()

    if re.match(r'(rising|hearmeneigh|mrstallion)', args.agent, flags=re.IGNORECASE):
        username = os.getlogin()
        print(f'The user agent string must not contain words "rising", "hearmeneigh", or "mrstallion". Try --agent "dr-{username}/1.0 (by {username})" instead?')
        exit(1)

    return args


def get_unique_post_id(post: PostEntity) -> str:
    return f'{post.source.value if "value" in post.source else post.source}___{post.source_id}'


def main():
    args = get_args()

    print('Loading filters')
    prefilters = {key: True for key in load_yaml(args.prefilter).get('tags', [])}

    p = Progress('Loading samples', 'samples')
    selections = [SelectionSource(samples) for samples in args.samples]
    p.succeed('Samples loaded!')

    # remove duplicates
    print('Removing duplicates')
    for (index, selection) in enumerate(selections):
        if index > 0:
            original_count = len(selection.posts)
            before_sels = selections[0:index]
            before_posts = set([get_unique_post_id(post) for sel in before_sels for post in sel.posts])
            selection.posts = [post for post in selection.posts if get_unique_post_id(post) not in before_posts]

            if len(selection.posts) != original_count:
                print(f'Removed {original_count - len(selection.posts)} duplicates from {selection.filename}')


    # balance selections
    print('Balancing buckets')
    balance_selections(selections)

    # combine selections
    print('Combining buckets')
    posts = [post for sel in selections for post in sel.posts]

    for selection in selections:
        print(f'Using {len(selection.posts)} ({round(len(selection.posts)/len(posts)*100, 1)}%) from {selection.filename}')

    # prune and filter tags
    print('Pruning tags...')
    tag_counts = prune_and_filter_tags(posts, prefilters, args.min_posts_per_tag)

    print(f'Using {len(tag_counts)} tags')

    # remove excess tags from posts
    for post in posts:
        post.tags = [tag for tag in post.tags if tag_counts.get(tag, 0) >= args.min_posts_per_tag]

    # remove posts that have too few tags
    print('Pruning posts...')
    old_post_count = len(posts)
    posts = [post for post in posts if len(post.tags) >= args.min_tags_per_post]
    print(f'Pruned {old_post_count - len(posts)} posts')

    # save tags
    print('Saving tags...')
    if args.export_tags is not None:
        os.makedirs(os.path.dirname(args.export_tags), exist_ok=True)

        with open(args.export_tags, 'w') as fp:
            tag_dict = {tag_name: tag_count for tag_name, tag_count in tag_counts.items() if tag_count >= args.min_posts_per_tag}
            json.dump(tag_dict, fp, indent=2)

    # save autocomplete
    print('Saving autocomplete...')
    if args.export_autocomplete is not None:
        os.makedirs(os.path.dirname(args.export_autocomplete), exist_ok=True)
        (db, client) = connect_to_db()

        # process tags
        tag_normalizer = load_normalizer_from_database(db)

        with open(args.export_autocomplete, 'w') as csv_file:
            for (tag_name, tag_count) in tag_counts.items():
                tag = tag_normalizer.get(tag_name)

                if tag is None:
                    print(f'Unexpected tag not found in database: "{tag_name}"')
                    continue

                known_aliases = [t for t in [tag.v1_name, tag.v2_name, tag.v2_short, tag.origin_name] if t != tag.preferred_name]

                if tag.aliases is not None:
                    for alias in tag.aliases:
                        if alias != tag.preferred_name and alias.strip() != '':
                            known_aliases.append(alias)

                csv_file.write(f"{tag.preferred_name},{numeric_categories.get(tag.category, 0)},{tag_count},\"{','.join(set(known_aliases))}\"\n")

    # shuffle posts
    print('Shuffling posts...')
    random.shuffle(posts)

    # generate dataset
    print('Generating the dataset & downloading images...')
    ds = Dataset.from_generator(
      format_posts_for_dataset,
      features=datasets.Features(
        {
          "source_id": datasets.Value(dtype='string', id=None),
          "source": datasets.Value(dtype='string', id=None),
          "image": datasets.Image(),
          "tags": datasets.Sequence(datasets.Value(dtype='string', id=None)),
          "url": datasets.Value(dtype='string', id=None),
          "text": datasets.Value(dtype='string', id=None),
          "desc": datasets.Value(dtype='string', id=None),
          "selector": datasets.Value(dtype='string', id=None),
        }
      ),
      num_proc=args.num_proc,
      gen_kwargs={
            'posts': posts if args.limit is None else posts[0:args.limit],
            'agent': args.agent,
            'image_width': args.image_width,
            'image_height': args.image_height,
            'image_format': args.image_format,
            'image_quality': args.image_quality,
            'separator': args.separator
      }
    )

    # cast images
    p = Progress('Casting image column', 'images')
    ds.cast_column('image', datasets.Image())
    p.succeed('Image column cast complete')

    # embed bytes
    p = Progress('Embedding bytes for accurate shard sizing', 'bytes')
    initial_format = ds.format
    ds = ds.with_format("arrow")
    ds = ds.map(embed_table_storage, batched=True, num_proc=args.num_proc)
    ds = ds.with_format(**initial_format)
    p.succeed('Shard sizing complete')

    os.makedirs(args.output, exist_ok=True)
    ds.save_to_disk(args.output, max_shard_size='1GB', num_proc=args.num_proc)

    # upload to huggingface
    if args.upload_to_hf is not None:
        p = Progress(f'Uploading to Huggingface {args.upload_to_huggingface}', 'bytes')
        # max_shard_size must be < 2GB, or you will run into problems
        ds.push_to_hub(args.upload_to_huggingface, private=True, max_shard_size='1GB')
        p.succeed('Dataset uploaded to Huggingface')

    # upload to S3
    if args.upload_to_s3 is not None:
        p = Progress(f'Uploading to S3 {args.upload_to_s3}', 'bytes')
        s3_client = boto3.client('s3')
        p.succeed('Dataset uploaded to S3')

    print('Done!')
    print(f'Dataset created with {len(posts)} samples and {len(tag_counts)} tags')


if __name__ == "__main__":
    main()
