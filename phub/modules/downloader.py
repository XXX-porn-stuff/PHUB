'''
PHUB 4 download backends.
'''

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Generator, Callable

if TYPE_CHECKING:
    from ..core import Client

from .. import errors, consts

def _segment_wrap(client: Client,
                  url: str,
                  callback: Callable = None,
                  buffer: dict = None) -> bytes:
    '''
    Download a single segment.
    '''
    
    for _ in range(consts.DOWNLOAD_SEGMENT_MAX_ATTEMPS):
        
            segment = client.call(url, throw = False)
            
            if segment.ok:
                if buffer:
                    buffer[url] = segment.content
                    callback()
                
                return segment.content
        
    raise errors.MaxRetriesExceeded(segment.status_code, segment.text)

def default(client: Client,
            segments: Generator,
            callback: Callable = None) -> bytes:
    '''
    Simple download.
    '''
    
    buffer = b''
    
    segments = list(segments)
    length = len(segments)
    
    for i, url in enumerate(segments):
        buffer += _segment_wrap(client, url)
        callback(i + 1, length)
    
    return buffer

def threaded(client: Client,
             segments: Generator,
             callback: Callable) -> bytes:
    '''
    Threaded download.
    '''
    
    buffer = {}
    finished = False
    
    def update():
        '''
        Called by threads on finish.
        '''
        
        lb, lf = len(buffer), len(threads)
        
        callback(lb, lf)
        finished = lb >= lf
    
    # Create the threads
    threads = [threading.Thread(target = _segment_wrap,
                                args = [client, url, buffer])
               for url in segments]
    
    # Start the threads
    for thread in threads:
        thread.start()
    
    # Wait for threads
    while not finished: pass
    
    # Concatenate buffer
    video = b''
    
    for url in segments:
        video += buffer[url]
    
    return video
        
        

def FFMPEG(client: Client, segments: Generator) -> bytes:
    '''
    TODO
    '''
    
    # TODO
    

# EOF
    