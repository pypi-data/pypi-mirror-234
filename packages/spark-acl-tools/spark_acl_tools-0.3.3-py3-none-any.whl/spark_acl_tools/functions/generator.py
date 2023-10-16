def read_ns(uuaa=None, is_dev=None, path=None):
    import pandas as pd
    import os
    from spark_acl_tools.utils import BASE_DIR
    from spark_dataframe_tools import get_color_b
    import sys

    is_windows = sys.platform.startswith('win')
    ns_code = "dev" if is_dev else "pro"
    uuaa = str(uuaa).upper()
    dir_ns = os.path.join(BASE_DIR, "utils", "files", "ns.csv")
    if is_windows:
        dir_ns = dir_ns.replace("\\", "/")

    if path not in ("", None):
        df = pd.read_csv(path, sep="|")
    else:
        df = pd.read_csv(dir_ns, sep="|")
    df2 = df[df["UUAA"] == f"{uuaa}"]
    if df2.shape[0] == 0:
        print(get_color_b("No existe uuaa registrada agregar manualmente el NS"))
        return None
    else:
        ns = df2.iloc[0]['NS']
        ns = f"pe-{uuaa.lower()}.app-id-{ns}.{ns_code}"
        return ns


def get_replace_value(acl_name=None,
                      col=None,
                      uuaa_sandbox=None,
                      uuaa_master=None,
                      uuaa_master_read=None,
                      uuaa_raw=None,
                      uuaa_staging=None,
                      ns=None):
    if acl_name == "ACL_INGESTA_MASTER":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_master}", uuaa_master) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_INGESTA_RAW":
        UUAA = str(uuaa_raw).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_raw}", uuaa_raw) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_PROCESAMIENTO_MASTER":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_master}", uuaa_master) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_RAW":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_master}", uuaa_master) \
            .replace("{uuaa_raw}", uuaa_raw) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_STAGING":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_master}", uuaa_master) \
            .replace("{uuaa_staging}", uuaa_staging) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_READ":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA) \
            .replace("{uuaa_master}", uuaa_master) \
            .replace("{uuaa_master_read}", uuaa_master_read) \
            .replace("{ns}", ns)
    elif acl_name == "ACL_MONITORING":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA)
    elif acl_name == "ACL_DATAPROC":
        UUAA = str(uuaa_master).upper()
        col = str(col).replace("{UUAA}", UUAA)
    elif acl_name == "ACL_SANDBOX":
        UUAA = str(uuaa_sandbox).upper()
        col = str(col).replace("{UUAA_SANDOX}", UUAA) \
            .replace("{uuaa_master}", uuaa_master)

    return col


def generated_acl_project_ingesta_master(uuaa_master=None,
                                         nro_ticket=None,
                                         is_dev=True,
                                         path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_INGESTA_MASTER"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_MASTER", col=x["Project"], uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_MASTER", col=x["Group"], uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_MASTER", col=x["Path"], uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_PROJECT_INGESTA_MASTER", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_project_ingesta_raw(uuaa_raw=None,
                                      nro_ticket=None,
                                      is_dev=True,
                                      path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_INGESTA_RAW"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_RAW", col=x["Project"], uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_RAW", col=x["Group"], uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_INGESTA_RAW", col=x["Path"], uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_PROJECT_INGESTA_RAW", uuaa_raw)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_raw}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_project_procesamiento_master(uuaa_master=None,
                                               nro_ticket=None,
                                               is_dev=True,
                                               path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_PROCESAMIENTO_MASTER"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_PROCESAMIENTO_MASTER", col=x["Project"],
                                    uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_PROCESAMIENTO_MASTER", col=x["Group"],
                                    uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_PROCESAMIENTO_MASTER", col=x["Path"],
                                    uuaa_master=uuaa_master, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_PROJECT_PROCESAMIENTO", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_raw(uuaa_master=None,
                           uuaa_raw=None,
                           nro_ticket=None,
                           is_dev=True,
                           path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_RAW"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_RAW", col=x["Project"], uuaa_master=uuaa_master,
                                    uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_RAW", col=x["Group"], uuaa_master=uuaa_master,
                                    uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_RAW", col=x["Path"], uuaa_master=uuaa_master,
                                    uuaa_raw=uuaa_raw, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_RAW", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_staging(uuaa_master=None,
                               uuaa_staging=None,
                               nro_ticket=None,
                               is_dev=True,
                               path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_STAGING"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_STAGING", col=x["Project"], uuaa_master=uuaa_master,
                                    uuaa_staging=uuaa_staging, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_STAGING", col=x["Group"], uuaa_master=uuaa_master,
                                    uuaa_staging=uuaa_staging, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_STAGING", col=x["Path"], uuaa_master=uuaa_master,
                                    uuaa_staging=uuaa_staging, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_STAGING", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_read(uuaa_master=None,
                            uuaa_master_read=None,
                            nro_ticket=None,
                            is_dev=True,
                            path=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    ns = read_ns(uuaa=uuaa_master, is_dev=is_dev, path=path)
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_READ"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_READ", col=x["Project"], uuaa_master=uuaa_master,
                                    uuaa_master_read=uuaa_master_read, ns=ns),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_READ", col=x["Group"], uuaa_master=uuaa_master,
                                    uuaa_master_read=uuaa_master_read, ns=ns),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_READ", col=x["Path"], uuaa_master=uuaa_master,
                                    uuaa_master_read=uuaa_master_read, ns=ns),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_READ", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_argos(uuaa_master=None,
                             nro_ticket=None,
                             is_dev=True):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_MONITORING"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_MONITORING", col=x["Project"], uuaa_master=uuaa_master),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_MONITORING", col=x["Group"], uuaa_master=uuaa_master),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_MONITORING", col=x["Path"], uuaa_master=uuaa_master),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_ARGOS", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_dataproc(uuaa_master=None,
                                nro_ticket=None,
                                is_dev=True):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "WORK" if is_dev else "LIVE"
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_DATAPROC"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_DATAPROC", col=x["Project"], uuaa_master=uuaa_master),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_DATAPROC", col=x["Group"], uuaa_master=uuaa_master),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_DATAPROC", col=x["Path"], uuaa_master=uuaa_master),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_DATAPROC", uuaa_master)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_master}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ruta_sandbox_live(uuaa_sandbox=None,
                                    uuaa_master=None,
                                    nro_ticket=None):
    import os
    from spark_dataframe_tools import get_color_b
    from spark_acl_tools.utils import BASE_DIR
    import pandas as pd
    import sys

    is_windows = sys.platform.startswith('win')
    sheet_name = "LIVE"
    file = os.path.join(BASE_DIR, "utils", "files", "acl.xlsx")
    if is_windows:
        file = file.replace("\\", "/")

    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    data = data[data["ACL_TYPE"] == "ACL_SANDBOX"]
    data["Project"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_SANDBOX", col=x["Project"],
                                    uuaa_sandbox=uuaa_sandbox, uuaa_master=uuaa_master),
        axis=1)
    data["Group"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_SANDBOX", col=x["Group"],
                                    uuaa_sandbox=uuaa_sandbox, uuaa_master=uuaa_master),
        axis=1)
    data["Path"] = data.apply(
        lambda x: get_replace_value(acl_name="ACL_SANDBOX", col=x["Path"],
                                    uuaa_sandbox=uuaa_sandbox, uuaa_master=uuaa_master),
        axis=1)
    data = data.drop(columns=['ACL_TYPE'])

    path_directory = os.path.join("DIRECTORY_ACL", "ACL_RUTA_SANDBOXLIVE", uuaa_sandbox)
    path_filename = os.path.join(path_directory, f"{sheet_name}- PE_UsuarioGrupo_DATASD-{nro_ticket}.xlsx")
    if is_windows:
        path_filename = path_filename.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    data.to_excel(path_filename, index=False, sheet_name='ACLs')

    print(get_color_b(f'GENERATED ACL UUAA: {uuaa_sandbox}'))
    print(f'create file for acl: {path_filename}')


def generated_acl_ticket_argos(domain="", uuaas=[], emails=[]):
    from spark_dataframe_tools import get_color_b

    print(get_color_b(f'Summary Argos WORK:'))
    print(get_color_b("TITLE"))
    if domain == "grm":
        print("[GRM][WORK-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "cs":
        print("[CLIENTS][WORK-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "fina":
        print("[FINANZAS][WORK-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "data":
        print("[DATA ENGINEERING][WORK-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "cib":
        print("[CIB/T&C/RIC][WORK-PE] Solicitud de accesos a ARGOS WORK")
    print("\n")
    print(get_color_b("DESCRIPTION"))
    print("Estimados, \n"
          "Favor de brindar accesos al grupo: \n")
    for uuaa in uuaas:
        print(f"DAPEW_US_MN{uuaa.upper()}")
    print("\n")
    for email in emails:
        print(f"{email}")

    print("\n\n")
    print(get_color_b(f'Summary Argos LIVE:'))
    print(get_color_b("TITLE"))
    if domain == "grm":
        print("[GRM][LIVE-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "cs":
        print("[CLIENTS][LIVE-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "fina":
        print("[FINANZAS][LIVE-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "data":
        print("[DATA ENGINEERING][LIVE-PE] Solicitud de accesos a ARGOS WORK")
    if domain == "cib":
        print("[CIB/T&C/RIC][LIVE-PE] Solicitud de accesos a ARGOS WORK")
    print("\n")
    print(get_color_b("DESCRIPTION"))
    print("Estimados, \n"
          "Favor de brindar accesos al grupo: \n")
    for uuaa in uuaas:
        print(f"DAPEL_US_MN{uuaa.upper()}")
    print("\n")
    for email in emails:
        print(f"{email}")

    print("\n\n")
    print("Link generated ticket:")
    print(get_color_b("https://jira.globaldevtools.bbva.com/servicedesk/customer/portal/40/create/1116"))


def generated_acl_ticket_dataproc(domain="", uuaas=[], emails=[]):
    from spark_dataframe_tools import get_color_b

    print(get_color_b(f'Summary Dataproc WORK:'))
    print(get_color_b("TITLE"))
    if domain == "grm":
        print("[GRM][WORK-PE] Solicitud de accesos a DATAPROC WORK")
    if domain == "cs":
        print("[CLIENTS][WORK-PE] Solicitud de accesos a DATAPROC WORK")
    if domain == "fina":
        print("[FINANZAS][WORK-PE] Solicitud de accesos a DATAPROC WORK")
    if domain == "data":
        print("[DATA ENGINEERING][WORK-PE] Solicitud de accesos a DATAPROC WORK")
    if domain == "cib":
        print("[CIB/T&C/RIC][WORK-PE] Solicitud de accesos a DATAPROC WORK")
    print("\n")
    print(get_color_b("DESCRIPTION"))
    print("Estimados, \n"
          "Favor de brindar accesos al grupo: \n")
    for uuaa in uuaas:
        print(f"DAPEW_US_DW{uuaa.upper()}")
    print("\n")
    for email in emails:
        print(f"{email}")

    print("\n\n")
    print(get_color_b(f'Summary Dataproc LIVE:'))
    print(get_color_b("TITLE"))
    if domain == "grm":
        print("[GRM][LIVE-PE] Solicitud de accesos a DATAPROC LIVE")
    if domain == "cs":
        print("[CLIENTS][LIVE-PE] Solicitud de accesos a DATAPROC LIVE")
    if domain == "fina":
        print("[FINANZAS][LIVE-PE] Solicitud de accesos a DATAPROC LIVE")
    if domain == "data":
        print("[DATA ENGINEERING][LIVE-PE] Solicitud de accesos a DATAPROC LIVE")
    if domain == "cib":
        print("[CIB/T&C/RIC][LIVE-PE] Solicitud de accesos a DATAPROC LIVE")
    print("\n")
    print(get_color_b("DESCRIPTION"))
    print("Estimados, \n"
          "Favor de brindar accesos al grupo: \n")
    for uuaa in uuaas:
        print(f"DAPEL_US_DR{uuaa.upper()}")
    print("\n")
    for email in emails:
        print(f"{email}")

    print("\n\n")
    print("Link generated ticket:")
    print(get_color_b("https://jira.globaldevtools.bbva.com/servicedesk/customer/portal/40/create/1116"))
