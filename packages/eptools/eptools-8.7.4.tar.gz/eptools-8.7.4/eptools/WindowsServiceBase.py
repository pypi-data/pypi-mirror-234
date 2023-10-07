'''
SMWinservice
by Davide Mastromatteo
Base class to create winservice in Python ~ https://github.com/eduardofaneli/PythonWinService/blob/master/SMWinservice.py
-----------------------------------------
Instructions:
1. Just create a new class that inherits from this base class
2. Define into the new class the variables
   _svc_name_ = "nameOfWinservice"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
3. Override the three main methods:
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
    def main(self)  : your actual run loop. Just create a loop based on your running condition
4. Define the entry point of your module calling the method "parse_command_line" of the new class
5. Enjoy
'''

'''
Documentation confluence:
- Deployment: https://easypost.atlassian.net/wiki/spaces/ITTEAM/pages/1096089601/Easypost+Library
'''

import datetime
import os
import socket
import sys
import time
import servicemanager
import win32event
import win32service
import win32serviceutil
import pyodbc
import subprocess
import re
import socket
from eptools.SQLFactory import SQLConnection, SQLFactory

# Custom imports
from .logger import EasyPostLogger

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = ''
    _svc_display_name_ = ''
    _svc_description_ = 'Python Service Description'
    _svc_logger_ = 'pythonService_logger'
    _looptime_ = 5
    # Execute run method once per day
    _daily_ = None
    _daily_minute_ = None
    # Execute run method every looptime from hour including to hour
    _daily_range_from_ = None
    _daily_range_to_ = None
    _no_weekend_ = False
    _one_run_ = None
    _svc_logpath_ = None
    _svc_config_path_ = 'C:\\Software\\Configs\\eptools.json'
    _location_ = str(socket.gethostname())

    # Execute exe instead of run method
    _csharp_exe_path_ = None
    args = []           # Contains args passed to service
    _args_extra_ = []     # Contains args overriden by child class to pass arguments

    logger = None
    
    finish_query = """
        DECLARE @status varchar(max) = ?;
        DECLARE @service_description varchar(max) = ?; 
        DECLARE @status_description varchar(max) = ?; 
        DECLARE @daily int = ?; 
        DECLARE @looptime int = ?; 
        DECLARE @dailyminute int = ?; 
        DECLARE @dailyrangefrom int = ?; 
        DECLARE @dailyrangeto int = ?; 
        DECLARE @noweekend int = ?; 
        DECLARE @onerun int = ?; 
        DECLARE @status_type varchar(10) = ?;
        
        IF EXISTS 
            (
                SELECT 1
                FROM EasyPostServices.dbo.Services 
                WHERE ServiceName = '{table}'
            )
                BEGIN
                    UPDATE EasyPostServices.dbo.Services 
                    SET 
                        ServiceDescription = @service_description,
                        LastFinishDateTime = GETDATE(),
                        LastFinishStatus = @status,
                        DailyHour = @daily,
                        DailyMinute = @dailyminute,
                        DailyRangeFrom = @dailyrangefrom,
                        DailyRangeTo = @dailyrangeto,
                        NoWeekend = @noweekend,
                        OneRun = @onerun,
                        ServiceType = 'PythonService'
                    WHERE ServiceName = '{table}'
                END
            ELSE
                BEGIN
                    INSERT INTO EasyPostServices.dbo.Services 
                    (ServiceName
                    ,ServiceDescription
                    ,StatusLogs
                    ,LastStartDateTime
                    ,LastRunDateTime
                    ,LastFinishDateTime
                    ,LastFinishStatus
                    ,LoopTime
                    ,DailyHour
                    ,DailyMinute
                    ,DailyRangeFrom
                    ,DailyRangeTo
                    ,NoWeekend
                    ,OneRun
                    ,ServiceType)
                    VALUES
                        (
                        '{table}'
                        ,@service_description
                        ,'EasyPostServices.dbo.{table}'
                        ,'1997-01-01 00:00'
                        ,'1997-01-01 00:00'
                        , GETDATE()
                        ,@status
                        ,@looptime
                        ,@daily
                        ,@dailyminute
                        ,@dailyrangefrom
                        ,@dailyrangeto
                        ,@noweekend
                        ,@onerun
                        ,'PythonService'
                        )
        END     
        ;
        IF NOT EXISTS(SELECT 1 FROM (SELECT TOP(1) * FROM EasyPostServices.dbo.{table} ORDER BY DateTime DESC) one WHERE  Type = @status_type AND Description = @status_description)
        BEGIN
            INSERT INTO EasyPostServices.dbo.{table}
                (DateTime
                ,Type
                ,Description)
            VALUES
                (GETDATE()
                ,@status_type
                ,@status_description)
        END
        ELSE
        BEGIN
            UPDATE EasyPostServices.dbo.{table}
            SET DateTime = GETDATE(),
                SequentialOccurrences = SequentialOccurrences + 1
            WHERE Id in (SELECT TOP(1) Id FROM EasyPostServices.dbo.{table} ORDER BY DateTime DESC)
        END
    """
    run_query = """
        DECLARE @status varchar(max) = ?;
        DECLARE @service_description varchar(max) = ?; 
        DECLARE @daily int = ?; 
        DECLARE @looptime int = ?;  
        DECLARE @dailyminute int = ?; 
        DECLARE @dailyrangefrom int = ?; 
        DECLARE @dailyrangeto int = ?; 
        DECLARE @noweekend int = ?; 
        DECLARE @onerun int = ?;
        DECLARE @location varchar(50) = ?; 

        IF EXISTS 
            (
                SELECT 1
                FROM EasyPostServices.dbo.Services 
                WHERE ServiceName = '{table}'
            )
                BEGIN
                    UPDATE EasyPostServices.dbo.Services 
                    SET 
                        ServiceDescription = @service_description,
                        LastRunDateTime = GETDATE(),
                        LastFinishStatus = @status,
                        DailyHour = @daily,
                        DailyMinute = @dailyminute,
                        DailyRangeFrom = @dailyrangefrom,
                        DailyRangeTo = @dailyrangeto,
                        NoWeekend = @noweekend,
                        OneRun = @onerun,
                        ServiceType = 'PythonService',
                        Location = @location
                    WHERE ServiceName = '{table}'
                END
            ELSE
                BEGIN
                    INSERT INTO EasyPostServices.dbo.Services 
                    (ServiceName
                    ,ServiceDescription
                    ,StatusLogs
                    ,LastStartDateTime
                    ,LastRunDateTime
                    ,LastFinishDateTime
                    ,LastFinishStatus
                    ,LoopTime
                    ,DailyHour
                    ,DailyMinute
                    ,DailyRangeFrom
                    ,DailyRangeTo
                    ,NoWeekend
                    ,OneRun
                    ,ServiceType
                    ,Location)
                    VALUES
                        (
                        '{table}'
                        ,@service_description
                        ,'EasyPostServices.dbo.{table}'
                        ,'1997-01-01 00:00'
                        ,GETDATE()
                        ,'1997-01-01 00:00'
                        ,@status
                        ,@looptime
                        ,@daily
                        ,@dailyminute
                        ,@dailyrangefrom
                        ,@dailyrangeto
                        ,@noweekend
                        ,@onerun
                        ,'PythonService'
                        ,@location
                        )
        END     
        ;
    """
    start_query = """
        DECLARE @status varchar(max) = ?;
        DECLARE @service_description varchar(max) = ?; 
        DECLARE @daily int = ?; 
        DECLARE @looptime int = ?; 
        DECLARE @dailyminute int = ?; 
        DECLARE @dailyrangefrom int = ?; 
        DECLARE @dailyrangeto int = ?; 
        DECLARE @noweekend int = ?; 
        DECLARE @onerun int = ?; 


        IF EXISTS 
        (
            SELECT 1
            FROM EasyPostServices.dbo.Services 
            WHERE ServiceName = '{table}'
        )
            BEGIN
                UPDATE EasyPostServices.dbo.Services 
                SET LastStartDateTime = GETDATE(),
                    ServiceDescription = @service_description,
                    StatusLogs = 'EasyPostServices.dbo.{table}',
                    LoopTime = @looptime,
                    DailyHour = @daily,
                    DailyMinute = @dailyminute,
                    DailyRangeFrom = @dailyrangefrom,
                    DailyRangeTo = @dailyrangeto,
                    NoWeekend = @noweekend,
                    OneRun = @onerun,
                    ServiceType = 'PythonService'
                    
                WHERE ServiceName = '{table}'
            END
        ELSE
            BEGIN
                INSERT INTO EasyPostServices.dbo.Services 
                (ServiceName
                ,ServiceDescription
                ,StatusLogs
                ,LastStartDateTime
                ,LastRunDateTime
                ,LastFinishStatus
                ,LoopTime
                ,DailyHour
                ,DailyMinute
                ,DailyRangeFrom
                ,DailyRangeTo
                ,NoWeekend
                ,OneRun
                ,ServiceType)
                VALUES
                    (
                    '{table}'
                    ,@service_description
                    ,'EasyPostServices.dbo.{table}'
                    ,GETDATE()
                    ,'1997-01-01 00:00'
                    ,'1997-01-01 00:00'
                    ,@looptime
                    ,@daily
                    ,@dailyminute
                    ,@dailyrangefrom
                    ,@dailyrangeto
                    ,@noweekend
                    ,@onerun
                    ,'PythonService'
                    )
            END
    """
    query_create_table = """
                    IF NOT EXISTS(SELECT 1 FROM EasyPostServices.sys.Tables WHERE  Name = N'{table}' AND Type = N'U')
                    BEGIN
                        CREATE TABLE  EasyPostServices.dbo.{table}(
                            Id int IDENTITY(1,1) NOT NULL,
                            DateTime datetime NOT NULL,
                            Type varchar(10) NOT NULL,
                            Description varchar(max) NOT NULL,
                            SequentialOccurrences int NOT NULL,
                            CONSTRAINT PK_{table} PRIMARY KEY CLUSTERED 
                        (
                            Id ASC
                        )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
                        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
                        
                        ALTER TABLE  EasyPostServices.dbo.{table} ADD  CONSTRAINT DF_{table}_Description  DEFAULT ('') FOR Description
                        ALTER TABLE EasyPostServices.dbo.{table} ADD  CONSTRAINT DF_{table}_SequentialOccurrences  DEFAULT ((1)) FOR SequentialOccurrences
                        SET ANSI_NULLS ON
                        SET QUOTED_IDENTIFIER ON
                    END
        """
    
    def connect_to_db(self,retry=0):
        try:
            sqlf = SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger=self.logger)
            sqlf.createConnection()
            db_conn = sqlf.connection
            return db_conn
        except pyodbc.Error as e:      
            if retry < 4:
                return self.connect_to_db(retry=retry+1)
            else:
                if self.logger:
                    self.logger.error(msg="SQL connection error to PRINTDB", ex=e)
                return False
    
    def setup_db(self,retry=0):
        db_conn = self.connect_to_db()
        if db_conn:
            try:
                cursor = db_conn.cursor()
                cursor.execute(self.query_create_table.format(table = self._svc_name_))
                cursor.commit()
                cursor.close()
                db_conn.close()
                return True
            except Exception as ex:
                if retry < 4:
                    return self.setup_db(retry=retry+1)
                else:
                    self.logger.error(msg="Starting Service DataBase Write Failed", ex=ex)
        return False

    def write_to_db(self,status = 'start', options=['FINISH','SUCCESS'],retry=0):
        db_conn = self.connect_to_db()
        # if self.logger:
        #     self.logger.debug("got db conn")
        # if self.logger:
        #     self.logger.debug(db_conn)
        if db_conn:
            try:
                with db_conn.cursor() as cursor:
                    if status == 'start':
                        qry_start = self.start_query.format(table=self._svc_name_)
                        # self.logger.debug("start_query\n" + qry_start)
                        cursor.execute(qry_start,(
                                options[0],  # status
                                self._svc_description_, #DECLARE @service_description varchar(max) = ?; 
                                self._daily_, # DECLARE @daily int = ?; 
                                self._looptime_, # DECLARE @looptime int = ?; 
                                self._daily_minute_, # DECLARE @dailyminute int = ?; 
                                self._daily_range_from_, # DECLARE @dailyrangefrom int = ?; 
                                self._daily_range_to_, # DECLARE @dailyrangeto int = ?; 
                                self._no_weekend_, # DECLARE @noweekend int = ?; 
                                self._one_run_ # DECLARE @onerun int = ?; 
                            )
                        )
                    if status == 'run':
                        qry_run = self.run_query.format(table=self._svc_name_)
                        # self.logger.debug("run_query\n" + qry_run)
                        cursor.execute(qry_run,(
                                options[0],  # status
                                self._svc_description_, #DECLARE @service_description varchar(max) = ?; 
                                self._daily_, # DECLARE @daily int = ?; 
                                self._looptime_, # DECLARE @looptime int = ?;  
                                self._daily_minute_, # DECLARE @dailyminute int = ?; 
                                self._daily_range_from_, # DECLARE @dailyrangefrom int = ?; 
                                self._daily_range_to_, # DECLARE @dailyrangeto int = ?; 
                                self._no_weekend_, # DECLARE @noweekend int = ?; 
                                self._one_run_, # DECLARE @onerun int = ?; 
                                self._location_
                            )
                        )
                    if status == 'finish':
                        qry_finish = self.finish_query.format(table=self._svc_name_)
                        # self.logger.debug("finish_query\n" + qry_finish)
                        cursor.execute(qry_finish,(
                                options[0],  # status
                                self._svc_description_, #DECLARE @service_description varchar(max) = ?; 
                                options[1],             #DECLARE @status_description varchar(max) = ?; 
                                self._daily_, # DECLARE @daily int = ?; 
                                self._looptime_, # DECLARE @looptime int = ?;  
                                self._daily_minute_, # DECLARE @dailyminute int = ?; 
                                self._daily_range_from_, # DECLARE @dailyrangefrom int = ?; 
                                self._daily_range_to_, # DECLARE @dailyrangeto int = ?; 
                                self._no_weekend_, # DECLARE @noweekend int = ?; 
                                self._one_run_, # DECLARE @onerun int = ?; 
                                'FINISH', # DECLARE @status_type varchar(10) = ?;    
                            )
                        )
                    if status == 'error':
                        qry_error = self.finish_query.format(table=self._svc_name_)
                        # self.logger.debug("error_query\n" + qry_error)
                        cursor.execute(qry_error,(
                                options[0],  # status
                                self._svc_description_, #DECLARE @service_description varchar(max) = ?; 
                                options[1],             #DECLARE @status_description varchar(max) = ?; 
                                self._daily_, # DECLARE @daily int = ?; 
                                self._looptime_, # DECLARE @looptime int = ?; 
                                self._daily_minute_, # DECLARE @dailyminute int = ?; 
                                self._daily_range_from_, # DECLARE @dailyrangefrom int = ?; 
                                self._daily_range_to_, # DECLARE @dailyrangeto int = ?; 
                                self._no_weekend_, # DECLARE @noweekend int = ?; 
                                self._one_run_, # DECLARE @onerun int = ?; 
                                'ERROR', # DECLARE @status_type varchar(10) = ?;    
                            )
                        )
                    cursor.commit()
                    return True
            except Exception as ex:
                if retry < 4:
                    return self.write_to_db(status = status, options= options,retry=retry+1)
                else:
                    self.logger.error(msg="Unable to write service time", ex=ex)

        return False

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)
    
    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        self.logger = EasyPostLogger(self._svc_name_, self._svc_logpath_, self._svc_config_path_)
        # self.logger.debug(self._svc_name_)
        # self.logger.debug(self._svc_display_name_)
        self.args = [arg for arg in args]
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        
    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.isrunning = False
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.isrunning = True
        # if self.logger:
        #         self.logger.debug("seting up db")
        if self.setup_db():
            pass
            # self.logger.debug("success setup")
        else:
            self.logger.error("failed setup")

        self.main()
        # if self.logger:
        #         self.logger.debug("passed main")

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        self.write_to_db(status='start')
        # if self.logger:
        #         self.logger.debug("written to db")
        if self._one_run_:
            self.write_to_db(status='run',options=["Started","Started"])
            try:
                # self.logger.debug("loop service: " + self._svc_name_)
                result = str(self.loop())
                self.write_to_db(status='finish',options=[result,result])
            except Exception as e:
                self.logger.error(msg="Exception executing run: ", ex=e)
                self.write_to_db(status='error',options=['FAIL',str(e)])

        elif self._daily_range_from_ and self._daily_range_to_:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now().hour >= self._daily_range_from_ and datetime.datetime.now().hour <= self._daily_range_to_:
                    if datetime.datetime.now() > checker:
                        checker += datetime.timedelta(seconds=self._looptime_)
                        self.write_to_db(status='run',options=["Started","Started"])
                        try:
                            # self.logger.debug("loop service: " + self._svc_name_)
                            result = str(self.loop())
                            self.write_to_db(status='finish',options=[result,result])
                        except Exception as e:
                            self.logger.error(msg="Exception executing run: ", ex=e)
                            self.write_to_db(status='error',options=['FAIL',str(e)])
                        if checker <= datetime.datetime.now():
                            checker = datetime.datetime.now()
                else:
                    checker = datetime.datetime.now().replace(hour=self._daily_range_from_,minute=0,second=0)
                time.sleep(1)
        elif self._daily_ != None and self._daily_ >= 0 and self._daily_ <= 23:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    # wait for 14h
                    checker += datetime.timedelta(seconds=self._looptime_)
                    if datetime.datetime.now().hour == self._daily_:
                        if self._daily_minute_ is not None:
                            if datetime.datetime.now().minute == self._daily_minute_:
                                checker += datetime.timedelta(hours=23,seconds=-self._looptime_ * 5)
                                self.write_to_db(status='run',options=["Started","Started"])
                                try:
                                    # self.logger.debug("loop service: " + self._svc_name_)
                                    result = str(self.loop())
                                    self.write_to_db(status='finish',options=[result,result])
                                except Exception as e:
                                    self.logger.error(msg="Exception executing run",ex=e)
                                    self.write_to_db(status='error',options=['FAIL',str(e)])
                                if checker <= datetime.datetime.now():
                                    checker = datetime.datetime.now()
                        else:
                            checker += datetime.timedelta(hours=23,seconds=-self._looptime_ * 5)
                            self.write_to_db(status='run',options=["Started","Started"])
                            try:
                                # self.logger.debug("loop service: " + self._svc_name_)
                                result = str(self.loop())
                                self.write_to_db(status='finish',options=[result,result])
                            except Exception as e:
                                self.logger.error(msg="Exception executing run",ex=e)
                                self.write_to_db(status='error',options=['FAIL',str(e)])
                            if checker <= datetime.datetime.now():
                                checker = datetime.datetime.now()
                time.sleep(1)
        else:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    try:
                        self.write_to_db(status='run',options=["Started","Started"])
                        # self.logger.debug("-----------started loop--" + str(checker) + "-----------")
                        result = str(self.loop())
                        self.write_to_db(status='finish',options=[result,result])
                        # self.logger.debug("-----------ended loop--" + str(checker) + "-----------")
                    except Exception as e:
                        self.logger.error(msg="Exception executing run: ", ex=e)
                        self.write_to_db(status='error',options=['FAIL',str(e)])
                    checker += datetime.timedelta(seconds=self._looptime_)
                    if checker <= datetime.datetime.now():
                        checker = datetime.datetime.now()
                time.sleep(1)
            
    def loop(self):
        weekend_checker = datetime.datetime.now().weekday()
        if weekend_checker > 4 and self._no_weekend_:
            return "Skipping loop weekend: " + str(weekend_checker)
        if self._csharp_exe_path_:
            return self.run_csharp_by_exe_path(self._csharp_exe_path_)
        return self.run()

    def run(self):
        '''
        Run to be overridden to add script
        '''
        raise NotImplementedError

    def run_csharp_by_exe_path(self, full_exe_path):
        """
        Statuscode to return:
        - 0: failure
        - 1: success

        To give value-able information (can only be used once):
        Console.WriteLine("FINALSTRING:<insert useful information>")
        """
        return_code = None
        stdout_line = 'Start'
        stderr_line = 'Start'
        finalstring = "No FinalString"

        if not os.path.exists(full_exe_path):
            self.logger.debug("Exe path does not exists...")
        else:
            self.logger.debug("Exe path: \n" + full_exe_path)

        # Build arguments
        exe_args = [] 
        exe_args.append(full_exe_path)                  # Execution path
        exe_args.append("--environment=Production")     # Environment will always be production
        # exe_args += self.args_extra 
        offset = 1   
                # Append the child arguments 
        for i in range(1, len( self.args)):
            offset += 1
            exe_args.append("--arg" + str(i) + "=" + str(self.args[i]))
        if len(self._args_extra_) > 0:
            for i in range(len(self._args_extra_)):
                exe_args.append("--arg" + str(offset + i) + "=" + str(self._args_extra_[i]))

        # Execute .EXE
        with subprocess.Popen(exe_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
            while return_code is None:
                # Read from console output
                # if self.logger:
                #     self.logger.debug("return_code is none")
                while stdout_line:
                    # if self.logger:
                    #     self.logger.debug("reading stdout")
                    stdout_line = process.stdout.readline()
                    if len(stdout_line):
                        if self.logger:
                            self.logger.debug(stdout_line)
                        # If matches custom regex, this message will written to database as "service log" which can be viewed in bull 
                        if re.search("^(FINALSTRING:){1}(.)*$",stdout_line):
                            if self.logger:
                                self.logger.debug(stdout_line)
                            finalstring = stdout_line[len("FINALSTRING:"):] # remove the "FINALSTRING:" from the line
                            if self.logger:
                                self.logger.debug(finalstring)
                        
                while stderr_line:
                    # if self.logger:
                    #         self.logger.debug("reading stderr")
                    stderr_line = process.stderr.readline()
                    if len(stderr_line):
                        if self.logger:
                            self.logger.error(msg=stderr_line)

                # fetch return value from .EXE (is an integer)
                return_code = process.poll()
                # if self.logger:
                #     self.logger.debug( return_code)
            process.stderr.close()
            process.stdout.close()

            if return_code == 1:
                
                success_msg = "Finished" 
            else:
                success_msg = "Failed"
                self.logger.error(finalstring)               
            
            return_message = success_msg + " with return code: " + str(return_code) + " finalstring: " + finalstring
            # if self.logger:
            #     self.logger.debug("return_message: " + return_message)
            return return_message

# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()