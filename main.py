import wx
from wx import MessageBox
from pypresence import Presence
from pubsub import pub
import json
import requests
import time

#read json file
with open('data.json', 'r') as file:
    data = json.load(file)

client_id = data['id']

# Create a class for the main window
class RichPresenceApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(RichPresenceApp, self).__init__(*args, **kw)

        # Set up the GUI layout
        self.init_ui()

        # Initialize RPC as None, to be connected later
        self.RPC = None

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("   Disconnected")

    def init_ui(self):
        panel = wx.Panel(self)

        # Labels and input fields
        wx.StaticText(panel, label="State:", pos=(20, 20))
        self.state_entry = wx.TextCtrl(panel, pos=(150, 20), size=(300, 25))

        wx.StaticText(panel, label="Details:", pos=(20, 60))
        self.details_entry = wx.TextCtrl(panel, pos=(150, 60), size=(300, 25))

        wx.StaticText(panel, label="Image Text:", pos=(20, 100))
        self.large_text_entry = wx.TextCtrl(panel, pos=(150, 100), size=(300, 25))

        wx.StaticText(panel, label="Image Path:", pos=(20, 140))
        self.large_image_entry = wx.TextCtrl(panel, pos=(150, 140), size=(300, 25))

        # Browse Image button
        browse_button = wx.Button(panel, label="Browse Image", pos=(460, 140))
        browse_button.Bind(wx.EVT_BUTTON, self.browse_image)

        # Connect to Discord button
        connect_button = wx.Button(panel, label="Connect to Discord", pos=(20, 200))
        connect_button.Bind(wx.EVT_BUTTON, self.start_presence)

        # Update Rich Presence button
        update_button = wx.Button(panel, label="Update Rich Presence", pos=(200, 200))
        update_button.Bind(wx.EVT_BUTTON, self.update_presence)

        # exit button
        exit_button = wx.Button(panel, label="Exit", pos=(380, 200))
        exit_button.Bind(wx.EVT_BUTTON, self.exit_button)

        # Set window properties
        self.SetTitle('Discord Rich Presence')
        self.SetSize((600, 300))
        self.Centre()

    def browse_image(self, event):
        # Open a file dialog to select an image file
        with wx.FileDialog(self, "Select Image", wildcard="PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg|All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # User canceled file selection

            # Get the selected file path and set it in the text entry
            self.large_image_entry.SetValue(fileDialog.GetPath())

    def start_presence(self, event):
        try:
            self.RPC = Presence(client_id)
            self.RPC.connect()
            wx.MessageBox(f"Connected to Discord!\nClient ID: {client_id}", "Success", wx.OK | wx.ICON_INFORMATION)
            self.status_bar.SetStatusText("   Connected to discord!")
        except Exception as e:
            wx.MessageBox(f"Failed to connect to Discord: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def update_presence(self, event):
        state = self.state_entry.GetValue()
        details = self.details_entry.GetValue()
        large_image = self.large_image_entry.GetValue()
        large_text = self.large_text_entry.GetValue()

        if self.RPC:
            try:
                self.RPC.update(
                    state=state,
                    details=details,
                    large_image=large_image,
                    large_text=large_text
                )
                wx.MessageBox("Rich Presence updated successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to update presence: {e}", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Not connected to Discord!", "Error", wx.OK | wx.ICON_ERROR)

    def exit_button(self, event):
        self.status_bar.SetStatusText("   exiting...")
        time.sleep(2)
        wx.CallAfter(frame.Destroy)
        
        
# Initialize the wxPython application
if __name__ == '__main__':
    app = wx.App()
    frame = RichPresenceApp(None)
    frame.SetMaxSize(wx.Size(600,300))
    frame.SetMinSize(wx.Size(600,300))

    frame.SetIcon(wx.Icon("resources\discord.ico"))

    frame.Show()
    app.MainLoop()
