
'''
Telling promopt what to do ofr terraform 


Terraform directory {terraform_dir}
Module type: {module_type} (local, remote)  --- Is module we are using create locally or are you using remote module like private module or public module
Backend config: {yes_or_no} -- Like AWS S3  ( Use state locking DDB , but S3 has locking now feature)
Steps to include:
    Format: {yes_or_no}
    Init: {yes_or_no}
    Validate: {yes_or_no}
    Plan: {yes_or_no} -- but as well terraform plan -output=file

'''

