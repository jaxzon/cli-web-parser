#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import requests

failures = []
successful_urls = []
total_urls = 0


@click.command()
@click.option('-i', '--image', help='Relative or absolute path to CSV filename')
def __main__(image):
    global total_urls
    click.echo('Parsing file: ' + image)
    with open(image, "r") as csv_file:
        for line in csv_file:
            total_urls += 1
            name, url = line.rstrip().split(';')
            response = make_request(name, url)
            if response:
                display_raw_html(response)
    display_summary()


def make_request(name, url):
    click.secho('HTML "' + name + '"', fg='magenta')
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as error:
        click.secho('Request failed to URL: ' + url, fg='red')
        click.secho(str(error), fg='red')
        failures.append({'url': url,
                         'error': error})
        return False
    response = parse_response(response, url)
    return response


def parse_response(response, url):
    if response.status_code == 200:
        successful_urls.append(url)
        return response
    else:
        error = 'Request failed with status code ' + str(response.status_code) + ' to URL: ' + url
        failures.append({'url': url,
                         'error': error})
        return False


def display_raw_html(response):
    raw_html = response.content
    click.echo(raw_html)


def display_summary():
    total_successful = len(successful_urls)
    click.secho('Successfully parsed ' + str(total_successful) + ' out of ' + str(total_urls) + ' URL\'s ', fg='green')
    if failures:
        total_failed = len(failures)
        failed_urls = [fail['url'] for fail in failures]
        click.secho('Failed to parse ' + str(total_failed) + ' URL\'s: ' + str(failed_urls), fg='red')
        for fault in failures:
            click.secho('Details: ' + fault['url'], fg='red')
            click.secho(str(fault['error']), fg='red')


if __name__ == '__main__':
    __main__()
