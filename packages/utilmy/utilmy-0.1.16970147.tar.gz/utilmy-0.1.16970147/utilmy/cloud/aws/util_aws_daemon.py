"""Daemon processes
Docs::

   Flush log on disk
   cd $utilmy/cloud/aws/
   python  util_aws_daemon.py   run_move_toS3 --freq 120  --format "%Y%M%D"   --dirin = loca/mylog/   --dirout  s3://bucket



"""
import time,  os
import boto3, awswrangler as wr
from pathlib import Path

from utilmy import date_now, log


########################################################################################################
########################################################################################################
def s3_files_move(dirin:str, dirout:str, use_threads=False, max_try=3):
    """ Uploads all the logfiles listed within dirin directory into S3 bucket/timestamp
    """
    dirin = Path(dirin)
    tmp_extn = ".dtmpXXX"
    for d in dirin.iterdir():
        if not d.is_file(): continue
        try :

            log(d) 
            dnew = d.rename(f"{d}{tmp_extn}")  if tmp_extn not in d.name else d

            local_file = dnew.absolute()
            path       = f'{dirout}/{dnew.name}'
            obj_list   = wr.s3.list_objects(path=path)
            if path in obj_list:
                path = f"{d.stem}.{int(time.time())}"  # To Avoid Overwrite : original filename + . + random alphabet
            wr.s3.upload(local_file=local_file, path=path, use_threads=use_threads)
            os.remove(local_file)
        except Exception as e:   #### It will pick on the next cycle
            log(e)
            time.sleep(5)

                       

def run_move_toS3(dirin, dirout, freq=600, add_datebucket=True, fmt="%Y%m%d", timezone="Asia/Japan"):
    """  Daemon moving logs to S3 in background
    Docs::
    
          python  main --freq 120  --format "%Y%m%d"   --dirin = loca/mylog/   --dirout  s3://bucket
    
    
    """                               
    while True:
        try :
        
            date0 = date_now(fmt=fmt, timezone=timezone)
            dirout= f"{dirout}/{date0}/" if add_datebucket else f"{dirout}/"
              
            s3_files_move(dirin=dirin, dirout=dirout)
            time.sleep(freq)
        except Exception as e: 
            log(e)

 

############################################################################################################
if __name__ == '__main__':
    import fire
    fire.Fire()




