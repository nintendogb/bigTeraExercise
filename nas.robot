*** Settings ***
Library    Collections
Library    DateTime
Library    HttpLibrary.HTTP
Library    RequestsLibrary
Library    DiffLibrary
Library    OperatingSystem
Library    ./diskspeed.py    WITH NAME    PF
*** Variable ***
${NAS_mount_point}    X:
${host}    192.168.192.130
${api_prefix}    :8080/cgi-bin/ezs3/
${fold_name}    tedTest
${user}    admin
${password}    admin
*** Test Cases ***
Login
    ${res}    RUN    curl -c cookie -k "https://${host}${api_prefix}login?user_id=${user}&password=${password}"
    Log    ${res}

Create share folder
    ${res}    RUN    curl -b cookie -k "https://${host}${api_prefix}create_shared_folder?name=${fold_name}&nfs=false&smb=true&read_only=false&mode=async"
    Log    ${res}
    Sleep    10s    Wait for create

mount NAS
    ${res}    RUN    net use ${NAS_mount_point} \\\\${host}\\${fold_name} /user:${user} ${password}
    LOG    ${res}
copy to NAS
    Copy Files    ./golden.txt    ${NAS_mount_point}/
diff file
    Diff Files     ./golden.txt    ${NAS_mount_point}/golden.txt
performance Test
    ${res}    PF.speedTest    ${NAS_mount_point}
    Log    ${res}
umount NAS
    ${res}    RUN    net use ${NAS_mount_point} /delete
    LOG    ${res}

Delete share folder
    ${res}    RUN    curl -b cookie -k "https://${host}${api_prefix}delete_shared_folder?name=${fold_name}"
    Log    ${res}

Check share folder had delete
    Directory Should Not Exist    ${NAS_mount_point}

