# spark_acl_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




spark_acl_tools is a Python library that implements for ACL
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-acl-tools 
```


## Usage

wrapper take ACLs

```sh
from spark_acl_tools import generated_acl_project_ingesta_master
from spark_acl_tools import generated_acl_project_ingesta_raw
from spark_acl_tools import generated_acl_project_procesamiento_master
from spark_acl_tools import generated_acl_ruta_argos
from spark_acl_tools import generated_acl_ruta_dataproc
from spark_acl_tools import generated_acl_ruta_raw
from spark_acl_tools import generated_acl_ruta_read
from spark_acl_tools import generated_acl_ruta_sandbox_live
from spark_acl_tools import generated_acl_ruta_staging



## GENERATED ACL PROJECT INGESTA MASTER
================================
uuaa_master = "pmfi"
nro_ticket = "45781"
generated_acl_project_ingesta_master(uuaa_master=uuaa_master, 
                                     nro_ticket=nro_ticket, 
                                     is_dev=True)




## GENERATED ACL PROJECT INGESTA RAW
================================
uuaa_raw = "pmfi"
nro_ticket = "45782"
generated_acl_project_ingesta_raw(uuaa_raw=uuaa_raw, 
                                  nro_ticket=nro_ticket, 
                                  is_dev=True)



## GENERATED ACL PROJECT PROCESAMIENTO MASTER
============================================================
uuaa_master = "pmfi"
nro_ticket = "45783"
generated_acl_project_procesamiento_master(uuaa_master=uuaa_master,
                                           nro_ticket=nro_ticket, 
                                           is_dev=True)
                               
                               
                               
## GENERATED RUTA RAW
============================================================
uuaa_master = "pmfi"
uuaa_raw = "l8px"
nro_ticket = "45784"

generated_acl_ruta_raw(uuaa_master=uuaa_master,
                       uuaa_raw=uuaa_raw,
                       nro_ticket=nro_ticket, 
                       is_dev=True)
                               
     
                               
## GENERATED RUTA STAGING
============================================================
uuaa_master = "pmfi"
uuaa_staging = "l8px"
nro_ticket = "45785"

generated_acl_ruta_staging(uuaa_master=uuaa_master,
                       uuaa_staging=uuaa_staging,
                       nro_ticket=nro_ticket, 
                       is_dev=True)
           
   
   
   
## GENERATED ACL RUTA LECTURA
============================================================
uuaa_master = "ppcw"
uuaa_master_read = "pbil"
nro_ticket = "45786"

generated_acl_ruta_read(uuaa_master=uuaa_master,
                       uuaa_master_read=uuaa_master_read,
                       nro_ticket=nro_ticket, 
                       is_dev=True)
                       
                       

## GENERATED ACL ARGOS
============================================================
uuaa_master = "ppcw"
nro_ticket = "45787"

generated_acl_ruta_dataproc(uuaa_master=uuaa_master,
                            nro_ticket=nro_ticket, 
                            is_dev=True)
                       
                       
## GENERATED ACL DATAPROC 
============================================================
uuaa_master = "ppcw"
nro_ticket = "45788"

generated_acl_ruta_dataproc(uuaa_master=uuaa_master,
                            nro_ticket=nro_ticket, 
                            is_dev=True)
                       
                       
## GENERATED ACL SANDBOX ONLY LIVE
#FINA,INC,MK8F,T1FL,OLNW,PAUD,PCDD,PCIB,PDPM,PESE,POPC,PTLC,RISK,TEST,
============================================================
uuaa_sandbox = "FINA"
uuaa_master = "ppcw"
nro_ticket = "45789"

generated_acl_ruta_sandbox_live(uuaa_sandbox=uuaa_sandbox, 
                                uuaa_master=uuaa_master, 
                                nro_ticket=nro_ticket)
  
```



## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
