#  obaxutils
#
#  version 0.1.6
#  utility functions for OBApps, OBHotkey, etc.
#  all xlib-dependent code goes here

license='''
Copyright (c) 2010 Eric Bohlman

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

from Xlib import X,display,Xcursorfont,Xatom
import Xlib.Xutil
import os

def get_ob_config_path():
    ds=display.Display()
    root=ds.screen().root
    p=root.get_full_property(ds.intern_atom('_OB_CONFIG_FILE'),ds.intern_atom('UTF8_STRING'))
    if p is None:
        path=os.path.expandvars('$HOME/.config/openbox/rc.xml')
    else:
        path=p.value
    if not os.path.isfile(path):
        print("creating new config file")
        try:
            os.makedirs(os.path.dirname(path))
        except OSError,ex:
            if not 'Errno 17' in str(ex):
                print("Error: Can't create ~/.config/openbox directory!"+str(ex))
                return
        if not os.path.isfile("/etc/xdg/openbox/rc.xml"):
            print( "Error: Couldn't find default config file!")
            self.Close()
            return
        try:
            orig = open("/etc/xdg/openbox/rc.xml", "r")
            dest = open(path,"w")
            dest.write(orig.read())
            orig.close()
            dest.close()
        except:
            print("Error: Couldn't create default config file!")
            return
    return path
    
def reconfigure_openbox():        
    ds=display.Display()
    root=ds.screen().root
    evt= Xlib.protocol.event.ClientMessage(display = ds, window = root,
            client_type = ds.intern_atom('_OB_CONTROL'), data = ( 32, ( 1, 0, 0, 0, 0 ) ) )
    ds.send_event(root, evt, event_mask = X.SubstructureNotifyMask | X.SubstructureRedirectMask)
    ds.flush()
        
def get_window_info(proplist):
    
    def find_client(win):
        if not hasattr(win,'get_full_property'):
            return
        if win.get_full_property(ds.intern_atom('_NET_WM_STATE'),Xatom.STRING) is not None:
            return win
        else:
            for w in win.query_tree().children:
                t=find_client(w)
                if t is not None:
                    return t
                
    ds=display.Display()
    root=ds.screen().root
    win=find_client(root.query_pointer().child)
    info=None
    if win is not None:
        info=[]
        for prop in  proplist:
            v=win.get_full_property(ds.intern_atom(prop),ds.intern_atom('UTF8_STRING')).value
            if v is None:
                v=''
            info.append(v)
    ds.close()
    return info

