#!/usr/bin/env python

from atlantic.aws import start_image_by_tag
from fabric.api import *
from fabric.api import settings
import sys


dget = "http://ftp.de.debian.org/debian/pool/main/f/fluxbox/fluxbox_1.3.2-4.dsc"


@task
def build():
    print "Finding & starting buildd machine."
    with start_image_by_tag("buildd") as instance:
        env.host_string = 'ubuntu@%s' % instance.dns_name
        env.key_filename = "/home/tag/.ssh/aws-prime.pem"

        wait_for_ssh()

        sudo("chown -R ubuntu:ubuntu logs")

        with settings(warn_only=True):
            run("dget %s" % (dget))

        run("sbuild -d unstable -v --source -A --source -j4 *dsc")

        print "Holding for inspection"
        print instance.dns_name
        sys.stdin.readlines()


def wait_for_ssh():
    try:
        run("echo 'foo'")
    except Exception:
        wait_for_ssh()
