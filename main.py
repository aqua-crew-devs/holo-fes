import sys
import uuid

from streamlink import Streamlink

def init_record(stream_url, cookies=""):
    filename = str('{}.ts'.format(uuid.uuid4()))
    print('task {} is began'.format(filename))
    session = Streamlink()
    if cookies != '':
        session.set_option('http-cookies', cookies)
        print('cookies is set to {}'.format(cookies))

    
    streams = session.streams(stream_url)
    source_stream = streams["best"]
    stream_fd = source_stream.open()
    os.makedirs("records", exist_ok=True)

    total_byte_accepted = 0
    SIZE_OF_THUNK = 1024
    # report to callback when 1M data is accepted
    bytes_for_next_callback = 1024 * 1024
    with open("./records/{}".format(filename), "wb") as record_fd:
        while True:
            try:
                data = stream_fd.read(SIZE_OF_THUNK)
                record_fd.write(data)
                total_byte_accepted += SIZE_OF_THUNK
                bytes_for_next_callback -= SIZE_OF_THUNK

                if bytes_for_next_callback <= 0:
                    print('recording is continuing, total bytes received: {} bytes'.format(total_byte_accepted))
                    bytes_for_next_callback = 1024 * 1024

            except EOFError:
                print('Recoding finished, total size is {} bytes. File is {}.ts '.format(total_byte_accepted, filename))
                break

if __name__ == "__main__":
    num_args = len(sys.argv)
    
    stream_url = sys.argv[1]
    cookies = sys.argv[2] if num_args == 3 else ""

    while True:
        try:
            init_record(stream_url, cookies)
            break
        except Exception as e:
            print('Error {} occurred. Retrying'.format(e))
    
