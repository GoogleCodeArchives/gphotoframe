import gtk
from gettext import gettext as _

from ..base import PluginDialog
from ...utils.urlget import UrlGetWithProxy
from ...utils.config import GConf
from auth import FlickrAuth

class PluginFlickrDialog(PluginDialog):

    def _set_ui(self):
        self.dialog = self.gui.get_widget('plugin_netauth_dialog')
        self.label  = self.gui.get_widget('label_netauth')
        self.button_p = self.gui.get_widget('button_netauth_p')
        self.button_n = self.gui.get_widget('button_netauth_n')

        self.p_id = self.n_id = None

        api_key = '343677ff5aa31f37042513d533293062'
        secret = GConf().get_string('plugins/flickr/secret')
        perms = 'write'

        self.auth_obj = FlickrAuth(api_key, secret, perms)

    def _set_confirm_dialog(self, *args):
        text = _("You are connected to Flickr.com as %s.") % self.user_name
        p_label = _('_Switch User')
        n_label = gtk.STOCK_OK
        p_cb = self._set_authorize_dialog
        n_cb = self._cancel_cb

        self._set_dialog(text, p_label, n_label, p_cb, n_cb)

    def _set_authorize_dialog(self, *args):
        text = _("Gnome Photo Frame needs your authorization in order to view \
private photos or to add photos to favorites list on your Flickr.com account. \
Press the \"Authorize\" button to open a web browser and give Gnome Photo Frame \
the authorization. ")
        p_label = gtk.STOCK_CANCEL
        n_label = _('_Authorize')
        p_cb = self._cancel_cb
        n_cb = self._set_complete_dialog

        self._set_dialog(text, p_label, n_label, p_cb, n_cb)

    def _set_complete_dialog(self, widget):
        self.auth_obj._get_frob() # getfrob -> open browser
        text = _("Return to this dialog after you have finished the authorization \
process on Flickr.com and click the \"Complete Authorization\" button below")
        p_label = gtk.STOCK_CANCEL
        n_label = _('_Complete Authorization')
        p_cb = self._cancel_cb
        n_cb = self.comp

        self._set_dialog(text, p_label, n_label, p_cb, n_cb)

    def comp(self, *args):
        self.auth_obj.get_auth_token(self.last)

    def last(self, data):
        self.nsid = data['nsid']
        self.user_name = data['user_name']
        self.auth_token = data['auth_token']

        self.conf.set_string('plugins/flickr/nsid', data['nsid'])
        self.conf.set_string('plugins/flickr/user_name', data['user_name'])
        self.conf.set_string('plugins/flickr/full_name', data['full_name'])
        self.conf.set_string('plugins/flickr/auth_token', data['auth_token'])

        self._set_confirm_dialog()

    def _set_dialog(self, text, p_label, n_label, p_cb, n_cb):

        self.label.set_text(text)
        self.button_p.set_label(p_label)
        self.button_n.set_label(n_label)

        if self.p_id:
            self.button_p.disconnect(self.p_id)
            self.button_n.disconnect(self.n_id)

        self.p_id = self.button_p.connect('clicked', p_cb)
        self.n_id = self.button_n.connect('clicked', n_cb)

    def _cancel_cb(self, *args):
        self.dialog.destroy()

    def run(self):
        self._read_conf()

        if self.auth_token:
            self._set_confirm_dialog()
        else:
            self._set_authorize_dialog()

        # self.dialog.show()
        response_id = self.dialog.run()

        if response_id == gtk.RESPONSE_OK: 
            print "ok"
            # self._write_conf()

        return response_id, {}

    def _read_conf(self):
        self.nsid = self.conf.get_string('plugins/flickr/nsid') # nsid
        self.user_name = self.conf.get_string('plugins/flickr/user_name')
        self.auth_token = self.conf.get_string('plugins/flickr/auth_token')

    def _write_conf(self):
        pass
