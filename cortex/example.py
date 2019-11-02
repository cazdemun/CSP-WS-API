import asyncio
from lib.cortex import Cortex

LICENSE_ID = "82a67d9d-b24b-4c11-a470-2868748a876b"
# LICENSE_ID = "e23653c4-1e33-4cdd-9009-d389859633e2"

# async def do_stuff(cortex):
#     # await cortex.inspectApi()
#     # print("** USER LOGIN **")
#     # await cortex.get_user_login()
#     # print("** GET CORTEX INFO **")
#     # await cortex.get_cortex_info()
#     # print("** HAS ACCESS RIGHT **")
#     # await cortex.has_access_right()
#     # print("** REQUEST ACCESS **")
#     # await cortex.request_access()
#     print("** AUTHORIZE **")
#     await cortex.authorize(license_id=LICENSE_ID,debit=50)
#     # await cortex.authorize(debit=50)
#     # print("** GET LICENSE INFO **")
#     # await cortex.get_license_info()
#     print("** QUERY HEADSETS **")
#     await cortex.query_headsets()

#     if len(cortex.headsets) < 1:
#       return 0
    
#     print("** CREATE SESSION **")
#     await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
#     print("** CREATE RECORD **")
#     await cortex.create_record(title="test record 1")
#     print("** SUBSCRIBE POW & MET **")
#     # await cortex.subscribe(['pow', 'met', 'eeg'])
#     await cortex.subscribe(['eeg'])
#     while cortex.packet_count < 10:
#         await cortex.get_data()
#     await cortex.inject_marker(label='halfway', value=1,
#                                 time=cortex.to_epoch())
#     while cortex.packet_count < 20:
#         await cortex.get_data()
#     await cortex.close_session()

async def do_stuff(cortex):
    print("** AUTHORIZE **")
    await cortex.authorize(license_id=LICENSE_ID,debit=50)
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()

    if len(cortex.headsets) < 1:
      return 0

    await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
    await cortex.create_record(title="emotiv raw test 1")
    
    
    await cortex.query_records()
    print(cortex.current_record)
    # await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
    # print("** QUERY SESSIONS **")
    # await cortex.query_sessions()
    # await cortex.close_session()
    # print("** QUERY SESSIONS **")
    # await cortex.query_sessions()

    # print("** CREATE SESSION **")
    # await cortex.create_session(activate=True, headset_id=cortex.headsets[0])
    # print("** CREATE RECORD **")
    # await cortex.create_record(title="test record 1")
    # print("** SUBSCRIBE POW & MET **")
    # await cortex.subscribe(['eeg'])

    # while cortex.packet_count < 10:
    #     await cortex.get_data()
    # await cortex.inject_marker(label='halfway', value=1,
    #                             time=cortex.to_epoch())
    # while cortex.packet_count < 20:
    #     await cortex.get_data()

    # await cortex.close_session()


def test():
    cortex = Cortex('./cortex_creds')
    asyncio.run(do_stuff(cortex))
    cortex.close()


if __name__ == '__main__':
    test()
