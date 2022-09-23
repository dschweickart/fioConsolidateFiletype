import time

from frameioclient import FrameioClient

VERBOSE = False

def consolidate(token, projectID, target_folder, file_ext):

    API_THROTTLE = 0.5

    client = FrameioClient(token)

    project = client.projects.get(projectID)
    time.sleep(API_THROTTLE)

    accountID = project['root_asset']['account_id']
    account = client._api_call('get', '/accounts/%s' % accountID, {})
    time.sleep(API_THROTTLE)

    target = client.assets.get(target_folder)
    time.sleep(API_THROTTLE)

    print(f"Account Name: {account['display_name']}")
    print(f"Project Name: {project['name']}")
    print(f"Consolidate to: {target['name']}")

    query = {"sort": "-inserted_at",
        "q" : file_ext ,
        "filter": {
            "project_id": {
                "op": "eq",
                "value": projectID}
            },
        "page_size": 10000,
        "account_id": accountID,
        "include" : "children"
        }

    print(f'Scanning Frameio project for {file_ext} files...(may take a minute)')
    scan_start = time.time()
    scan = client._api_call('post' , '/search/assets' , query)
    time.sleep(API_THROTTLE)

    elapsed = time.time() - scan_start
    print(f'Scan Complete in {int(elapsed)}sec')

    mxfCount = 0

    print('Checking destination directory for existing files...')
    target_contents = client.assets.get_children(target_folder)
    time.sleep(API_THROTTLE)
    existing_files = [x['name'] for x in target_contents]

    
    copyList = []

    for s in scan:

        if s['name'].lower().endswith(file_ext):
            mxfCount += 1

        if not any([x for x in existing_files if s['name'] == x]):
            
            copyList.append(s['id'])

            # try:
            #     copy = client.assets.copy(target_folder, s['id'])
            #     time.sleep(API_THROTTLE)
            # except Exception as e:
            #     print(f'ERROR ON FILE COPY: {e}')
            
            copy = 'NEW_COPY'
        else:
            copy = 'COPY_EXISTS'
        
        if VERBOSE:
            print(f"{s['name']} | mxfCount={mxfCount} | copyStatus={copy}")

    print(f'{len(scan)} {file_ext} files found. {len(copyList)} new files to copy.')

    if len(copyList):
        bsize = 500
        batchList = [copyList[i:i+bsize] for i in range(0, len(copyList), bsize)]
        print(f'Batchsize = {bsize} files')

        batch_num = 1    
        for batch in batchList:
            print(f'Batch-{batch_num} Copying New Files...')

            batch_start = time.time()
            batch = client.assets.bulk_copy(target_folder, batch)

            elapsed = time.time() - batch_start
            print(f'Copy Complete in {int(elapsed)}sec')
            batch_num += 1

if __name__ == '__main__':
    
    import sys

    args = []
    for x in range(5):
        try:
            args.append(sys.argv[x+1])
        except:
            args.append(None)

    token =         args[0] if args[0] else "fio-u-e3Exo-x8eeWyD2-8G9XjxwD9hAk9VWSBb2XeuK_3Kq1-KKgxb66xhMlGEU24Ime-"
    projectID =     args[1] if args[1] else 'aef0e6cf-2099-4400-97bf-0b210c710543'
    target_folder = args[2] if args[2] else '3a5ee321-00f0-4e4c-a187-ebf5f0ae309d' #'059419e6-83aa-4e55-b707-aa0c2d276e02'
    file_ext =      args[3] if args[3] else '.mxf'

    consolidate(token, projectID, target_folder, file_ext)
