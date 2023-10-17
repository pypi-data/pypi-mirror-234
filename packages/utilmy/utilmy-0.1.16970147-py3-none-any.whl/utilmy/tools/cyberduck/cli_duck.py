""" Ducke Download
Docs::

### manage Secreat 



##### Using pydrive   ################################################################################
Please copy the Google json auth in same folder than scripot

https://console.cloud.google.com/apis/dashboard

client_secrets.json


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)


####
Your browser has been opened to visit:

    https://accounts.google.com/o/oauth2/auth?client_id=132171571023-bcjjt9cohln6l0gejs9rh1vfe6bq7rrn.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&response_type=code




fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList:
  print('Title: %s, ID: %s' % (file['title'], file['id']))
  # Get the folder ID that you want
  break














https://tianhaozhou.medium.com/fill-the-gap-of-credential-management-in-github-actions-a313e230e58b



    C:\Program Files\Cyberduck CLI\




    ##### Dataset  from google
    duck --list "googledrive:/My Drive/dataset/"  --username emial@gmail.com  


Connection Profiles
You can install additional connection profiles in the application support directory. Use the --profile option
 to reference a connection profile file to use not installed in the standard location.

Linux
The support directory is ~/.duck/ on Linux. You can install third party profiles in ~/.duck/profiles/.

Install additional profiles in %AppData%\Cyberduck\Profiles on Windows.

Google Drive.cyberduckprofile


wget  https://dist.duck.sh/

wget https://dist.duck.sh/duck_8.4.3.38269-1_arm64.deb




    duck --list "googledrive:/My Drive/dataset/"  --profiles  mygoogledrive.xml   --username myemai@gmail.com 


    Command Line Interface (CLI)
    Cyberduck with a command-line interface (CLI) is available for Mac, Windows & Linux. It is installed as duck.

    Installation
    macOSWindowsLinux
    Chocolatey

    Available as a Chocolatey package. Use

    choco install duck
    to install.

    MSI Installer

    Download the latest setup.

    Snapshot Builds

    Not currently available.

    CLI Setup
    Usage
    Usage:duck [options...]

    Run --help to get the option screen.

    URLs in arguments must be fully qualified. Paths can either denote a remote file ftps://user@example.net/resource or folder ftps://user@example.net/directory/ with a trailing slash. You can reference files relative to your home directory with /~ftps://user@example.net/~/.

    Connection Profiles
    You can install additional connection profiles in the application support directory. Use the --profile option to reference a connection profile file to use not installed in the standard location.

    URI
    The <url> argument for --copy, --download, --upload, and --synchronize must satisfy following rules:

    Each URL must start with a scheme and a colon (https:)(unless you specify a --profile)

    Depending on the type of protocol you are referencing different rules apply

    For all protocols where no default hostname is set (e.g. WebDAV, SFTP, and FTPS) you must use a fully qualified URI https://user@hostname/path

    For all protocols where a default hostname is set, but you are allowed to change it (e.g. S3) you may use fully qualified URIs or Absolute paths: s3:/bucket/path, Relative paths: s3:user@path or s3:user@/path. Omitting the first slash in a relative path uses the default home directory for this protocol.

    For all protocols where a default hostname is set and you are not allowed to change it (e.g. OneDrive, Dropbox, Google Drive) you may use any combination of the above with the following rules: Fully Qualified URIs are parsed as relative paths. onedrive://Some/Folder/ is parsed as onedrive:Some/Folder.

    For all protocols where a default path is set and you are not allowed to change it (e.g. accessing a prebuilt NextCloud profile with a path set to /remote.php/webdav). You are allowed to change the path but it will be appended to the default path. Making nextcloud:/path really nextcloud:/remote.php/webdav/path.

    Note

    Spaces and other special-characters are not required to be percent-encoded (e.g. %20 for space) as long as the path is quoted duck --upload "scheme://hostname/path with/spaces" "/Path/To/Local/File With/Spaces".

    Protocol

    Fully Qualified URI required

    Absolute Path

    Relative Path

    Windows Azure Storage

    No

    azure:/<container>/<key>

    azure:<container>/<key>

    Backblaze B2 Cloud Storage

    No

    b2:/<container>/<key>

    b2:<container>/<key>

    WebDAV (HTTP)

    Yes (dav://<hostname>/<path>)

    WebDAV (HTTPS)

    Yes (dav://<hostname>/<path>)

    Dracoon (Email Address)

    Yes (dracoon://<hostname>/<path>)

    Dropbox

    No

    dropbox:/<path>

    dropbox:<path>

    Local

    No

    file:/<path>

    file:<path>

    FTP (File Transfer Protocol)

    Yes (ftp://<hostname>/<path>)

    FTPS (Explicit Auth TSL)

    Yes (ftps://<hostname>/<path>)

    Google Drive

    No

    googledrive:/<path>

    googledrive:<path>

    Google Cloud Storage

    No

    gs:/<path>

    gs:<path>

    Microsoft OneDrive

    No

    onedrive:/<path>

    onedrive:<path>

    Amazon S3

    s3://<hostname>/<container>/<key>

    s3:/<container>/<key>
    (using s3.amazonaws.com)

    s3:<container>/<key>
    (using s3.amazonaws.com)

    SFTP (SSH File Transfer
    Protocol)

    Yes (sftp://<hostname>/<path>)

    Spectra S3 (HTTPS)

    Yes
    (spectra://<hostname>/<container>/<key>)

    Rackspace Cloud Files (US)

    No

    rackspace:/<container>/<key>

    rackspace:<container>/<key>

    Swift (OpenStack Object
    Storage)

    Yes (swift://<hostname>/<container>/<key>)

    Examples
    List all buckets in S3 with

    duck --username <Access Key ID> --list s3:/
    List all objects in a S3 bucket with

    duck --username <Access Key ID> --list s3:/<bucketname>/
    Generic Options
    --retry
    Retry requests with I/O failures once per default. Useful on connnection timeout or latency issues.

    --verbose
    Print protocol transcript for requests and responses. This includes the HTTP headers.

    --nokeychain
    Do not save passwords in login keychain (macOS), credentials manager (Windows), or plain text password file (Linux).

    --quiet
    Suppress progress messages.

    --throttle
    Throttle bandwidth to the number of bytes per second.

    Credentials
    You can pass username as part of the URI prepending to the hostname with username@host. Alternatively, use the --username option. You can give the password with the --password option or you will be prompted before the connection is opened by the program if no password matching the host is found in your login keychain (OS X) or user configuration shared with Cyberduck (Windows).

    Private Key
    When connecting with SFTP you can give a file path to a private key with --identity for use with public key authentication.

    Tenant Name
    When connecting with OpenStack Swift you can set the tenant name (OpenStack Identity Service, Keystone 2.0) or project (OpenStack Identity Service, Keystone 3.0) with --username <tenant>:<user>.

    Downloads with --download
    Glob pattern support for selecting files to transfer
    You can transfer multiple files with a single command using a glob pattern for filename inclusion such as

    duck --download ftps://<hostname>/directory/*.css
    Uploads with --upload
    Glob Pattern Support for Selecting Files to Transfer
    If your shell supports glob expansion you can use a wildcard pattern to select files for upload like

    duck --upload ftps://<hostname>/directory/ ~/*.jpg
    Use of ~
    You can use the tilde to abbreviate the remote path pointing to the remote home folder as in sftp://duck.sh/~/. It will be expanded when constructing absolute paths.

    Remote Directory Listing with --list
    Make sure to include a trailing ‘/’ in the path argument to denote a directory. Use the -L option to print permission mask and modification date in addition to the filename.

    Edit with --edit
    You can edit remote files with your preferred editor on your local system using the --edit command. Use the optional --application option to specify the absolute path to the external editor you want to use.

    Purge Files in CDN with --purge
    Purge files in CloudFront or Akamai CDN for Amazon S3 or Rackspace CloudFiles connections. For example to invalidate all contents in a bucket run

    duck --username AKIAIWQ7UM47TA3ONE7Q --purge s3:/github-cyberduck-docs/
    Multiple Transfer Connections with --parallel
    Transfer files with multiple concurrent connections to a server.

    Cryptomator
    Access to your Cryptomator Vaults from the command line. When accessing a vault using --download, --list or --upload, you will be prompted to provide the passphrase for the Vault if not found in the Keychain.

    Use --vault <path> in conjunction with --upload to unlock a Vault. This allows uploading into a subdirectory of a Vault where the auto-detect feature does otherwise not work.

    Samples
    Watching Changes in Directory with fswatch and Upload
    fswatch is a file change monitor; an application to watch for file system changes. Refer to their documentation.

    fswatch -0 ~/Sites/mywebsite/ | xargs -0 -I {} -t sh -c 'f="{}"; duck --upload ftps://<hostname>/sandbox`basename "${f}"` "${f}" -existing overwrite'
    Upload Build Artifacts from Continuous Integration (Jenkins) to CDN
    use a post build script action.

    cd ${WORKSPACE}; find build -name '*.tar' -print0 | xargs -0 -I {} -t sh -c 'f="{}"; duck --quiet --retry --existing skip --region DFW --upload rackspace://<container>/ "${f}"'
    Upload Files Matching Glob Pattern to Windows Azure
    duck --username kahy9boj3eix --upload azure://kahy9boj3eix.blob.core.windows.net/<containername>/ *.zip
    Download Files Matching Glob Pattern from S3
    duck --user anonymous --verbose --download s3:/profiles.cyberduck.io/Wasabi* ~/Downloads/
    Download File from Amazon S3 Public Bucket
    duck --user anonymous --download s3:/repo.maven.cyberduck.io/releases/ch/cyberduck/s3/6.1.0/s3-6.1.0.jar ~/Downloads/
    Application Support Directory
    Profiles
    The directory location is printed with --help following the list of supported protocols.

    macOSWindowsLinux
    Install additional profiles in %AppData%\Cyberduck\Profiles on Windows.

    Preferences
    macOSWindowsLinux
    You can override default preferences by setting environment variables in your shell.

    set "property.name=value" & duck

    Known Issues
    Slow Execution due to low Entropy in /dev/random
    As a workaround run haveged, a service to generate random numbers and feed Linux random device.

    Third-Party References
    Using Cyberduck and duck CLI to access Oracle Cloud Infrastructure Classic Storage

  

  """