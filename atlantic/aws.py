#!/usr/bin/env python

from contextlib import contextmanager
import boto
import time

ec2 = boto.connect_ec2()


@contextmanager
def start_image_by_tag(image_name, terminate=True, owner="251399821276"):
    images = ec2.get_all_images(owners=[owner])
    for image in images:
        if "class" in image.tags:
            if image.tags['class'] == image_name:
                ami = image.id
                with start_server(
                    terminate=terminate,
                    image_id=ami
                ) as instance:
                    yield instance


@contextmanager
def start_server(terminate=True, **kwargs):
    kwargz = {
        "image_id": "ami-81c771e8",
        "key_name": "aws-prime",
        "instance_type": "t1.micro",
        "placement": "us-east-1a",
        "security_groups": [
            'buildd'
        ]
    }
    kwargz.update(kwargs)
    reservation = ec2.run_instances(**kwargz)
    instance = reservation.instances[0]
    instance.update()

    while instance.state == 'pending':
        time.sleep(1)
        instance.update()

    try:
        try:
            yield instance
        except Exception as e:
            print "Exception during runtime: %s" % (e)
    finally:
        print "Shutting down..."

        if not terminate:
            instance.stop()
        else:
            instance.terminate()

        instance.update()
        while instance.state == 'shutting-down':
            time.sleep(1)
            instance.update()
