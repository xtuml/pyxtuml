# encoding: utf-8
# Copyright (C) 2017 John Törnblom
#
# This file is part of pyxtuml.
#
# pyxtuml is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pyxtuml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with pyxtuml. If not, see <http://www.gnu.org/licenses/>.

import datetime
import sys
import time


class LOG(object):
    
    @staticmethod
    def LogInteger(message):
        print('LogInteger: %d' % message)

    @staticmethod
    def LogReal(message, r):
        print('LogReal: %f %s' % (r, message))
        
    @staticmethod
    def LogInfo(message):
        print('LogInfo: %s' % message)
        
    @staticmethod
    def LogFailure(message):
        print('LogFailure: %s' % message)
        
    @staticmethod
    def LogSuccess(message):
        print('LogSuccess: %s' % message)
        

class TIM(object):
    
    @staticmethod
    def create_date(day, hour, minute, month, second, year):
        return datetime.datetime(year, month, day, hour, minute, second)
    
    @staticmethod
    def current_date():
        return datetime.datetime.now()
    
    @staticmethod
    def current_clock():
        return time.time()
    
    @staticmethod
    def get_year(date):
        return date.year
    
    @staticmethod
    def get_month(date):
        return date.month
    
    @staticmethod
    def get_day(date):
        return date.day
    
    @staticmethod
    def get_hour(date):
        return date.hour
    
    @staticmethod
    def get_minute(date):
        return date.minute
    
    @staticmethod
    def get_second(date):
        return date.second
    
    
class ARCH(object):
    
    @staticmethod
    def shutdown():
        sys.exit()
        

class PERSIST(object):
    
    @staticmethod
    def commit():
        return 0
    
    @staticmethod
    def restore():
        return 0
    

class NVS(object):
    
    @staticmethod
    def format():
        return 0
    
    @staticmethod
    def version(first, second):
        return 0
    
    @staticmethod
    def checksum(first, second):
        return 0
        
