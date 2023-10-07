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

import uuid

from majormode.perseus.model.date import ISO8601DateTime


class Picture:
    def __init__(
            self,
            picture_id: uuid.UUID,
            picture_url: str,
            capture_time: ISO8601DateTime,
            update_time: ISO8601DateTime):
        """
        Build a picture instance.


        @param picture_id: The identification of the picture.

        @param picture_url: The Uniform Resource Locator (URL) that specifies
            the location of the picture.

        @param capture_time: The time when the picture was captured.

        @param update_time: The time of the most recent modification of one or
            more attribute of the picture.
        """
        self.__picture_id = picture_id
        self.__picture_url = picture_url
        self.__capture_time = capture_time
        self.__update_time = update_time

    @property
    def capture_time(self) -> ISO8601DateTime:
        return self.__capture_time

    @property
    def picture_id(self) -> uuid.UUID:
        return self.__picture_id

    @property
    def picture_url(self) -> str:
        return self.__picture_url

    @property
    def update_time(self) -> ISO8601DateTime:
        return self.__update_time
