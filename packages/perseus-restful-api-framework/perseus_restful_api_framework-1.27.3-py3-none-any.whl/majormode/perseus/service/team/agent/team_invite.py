# Copyright (C) 2019 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from majormode.perseus.service.team.team_service import TeamService

import settings
import smtplib
import time

# Define the minimum time interval between sending batch of invites,
# in seconds.
MINIMUM_TIME_INTERVAL_BETWEEN_INVITE_SENDING = 10

if __name__ == "__main__":
    pass
    # print "Team Member Invite Email Sender"
    # print "Copyright (C) 2013 Majormode.  All rights reserved."
    #
    # while True:
    #     try:
    #         invites = TeamService().send_invites(settings.PLATFORM_BOTNET_APP_ID,
    #                 settings.PLATFORM_BOTNET_ACCOUNT_ID)
    #
    #         print '[INFO] The following users have been sent an invite email:'
    #         for invite in invites:
    #             print '\t• %(recipient_name)s (%(email_address)s) invited to team %(team_name)s' % \
    #                 { 'email_address': invite.email_address,
    #                   'recipient_name': invite.recipient_name,
    #                   'team_name': invite.team_name }
    #
    #         time.sleep(MINIMUM_TIME_INTERVAL_BETWEEN_INVITE_SENDING)
    #     except smtplib.SMTPDataError, error:
    #         print '[ERROR] %s; waiting for one day...' % error.smtp_error
    #         time.sleep(60 * 60 * 24)
    #     except:
    #         print '[ERROR] $s; waiting for one minute...' % error.smtp_error
    #         time.sleep(60)
