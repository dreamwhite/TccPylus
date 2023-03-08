
import json
import plistlib
import os
import subprocess
import wx
import wx.lib.scrolledpanel

capabilities = [#'All',
              'Accessibility',
              'AddressBook',
              'AppleEvents',
              'Calendar',
              'Camera', 
              'ContactsFull',
              'ContactsLimited',
              'DeveloperTool',
              'Facebook',
              'LinkedIn', 
              'ListenEvent',
              'Liverpool',
              'Location',
              'MediaLibrary',
              'Microphone',
              'Motion', 
              'Photos',
              'PhotosAdd',
              'PostEvent',
              'Reminders',
              'ScreenCapture',
              'ShareKit', 
              'SinaWeibo',
              'Siri',
              'SpeechRecognition',
              'SystemPolicyAllFiles', 
              'SystemPolicyDesktopFolder',
              'SystemPolicyDeveloperFiles',
              'SystemPolicyDocumentsFolder', 
              'SystemPolicyDownloadsFolder',
              'SystemPolicyNetworkVolumes',
              'SystemPolicyRemovableVolumes', 
              'SystemPolicySysAdminFiles',
              'TencentWeibo',
              'Twitter',
              'Ubiquity',
              'Willow'
]

enabled_capabilities = list()


class CapabilitiesDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Capabilities")

        # Read the saved capabilities from the JSON file
        try:
            with open("saved_capabilities.json", "r") as f:
                data = json.load(f)
                saved_capabilities = {
                    capability["name"]: capability["checked"]
                    for capability in data["capabilities"]
                }
        except FileNotFoundError:
            saved_capabilities = {}

        # Create a scrollable panel
        panel = wx.lib.scrolledpanel.ScrolledPanel(self)
        panel.SetupScrolling()

        checkboxes = []
        self.Hide()
        sizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(0,len(capabilities)-1):
            checkbox = wx.CheckBox(panel, label=capabilities[i])
            if checkbox.GetLabel() in saved_capabilities:
                checkbox.SetValue(saved_capabilities[checkbox.GetLabel()])
            sizer.Add(checkbox, 0, wx.ALL | wx.ALIGN_CENTER, 5)
            checkboxes.append(checkbox)
        
        
        #TODO: If "All" is selected, select all the checkboxes
        panel.SetSizer(sizer)

        # Create a save button
        save_button = wx.Button(panel, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)

        # Add the button to a horizontal sizer
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.Add(save_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Add the button sizer and stretch spacer to the panel sizer
        sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        # Set the panel sizer
        panel.SetSizer(sizer)

        # Resize the dialog to fit all the checkboxes
        self.SetSize(800,600)
        self.SetAutoLayout(True)
        self.Show()

        # Set the checkboxes and save button as instance variables
        self.checkboxes = checkboxes
        self.save_button = save_button

    def on_save(self, event):
        # Save the status of all checkboxes to a JSON file
        data = {"capabilities": []}
        for checkbox in self.checkboxes:
                
            data["capabilities"].append(
                {"name": checkbox.GetLabel(), "checked": checkbox.GetValue()}
            )
            if checkbox.GetValue():
                enabled_capabilities.append(checkbox.GetLabel())
        with open("saved_capabilities.json", "w") as f:
            json.dump(data, f)
        self.Close()

class MyApp(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Main Window")

        self.select_app_btn = wx.Button(self, label="Select app")
        self.select_app_btn.Bind(wx.EVT_BUTTON, self.on_select_app)

        self.select_capabilities_btn = wx.Button(self, label="Select Capabilities")
        self.select_capabilities_btn.Bind(wx.EVT_BUTTON, self.on_select_capabilities)
        self.select_capabilities_btn.Disable()


        self.run_btn = wx.Button(self, label="Run program")
        self.run_btn.Bind(wx.EVT_BUTTON, self.on_run)
        self.run_btn.Disable()

        close_btn = wx.Button(self, label="Quit program")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)


        sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self.select_app_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.select_capabilities_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.Add(self.run_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.AddStretchSpacer()
        sizer.Add(close_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer.AddStretchSpacer()
        self.SetSizer(sizer)
        self.CFBundleIdentifier:str = ''

    def on_select_app(self, event):
        wildcard = "Mac Applications (*.app)|*.app"
        dlg = wx.FileDialog(
            self, message="Select an application", defaultDir='/Applications', 
            wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.app_path = dlg.GetPath()
            self.SetLabel(f'TccPylus - {self.app_path}')
            self.FindWindowByName("Select Capabilities").Enable()

        with open(os.path.join(self.app_path, 'Contents', 'Info.plist'), 'rb') as info:
            pl = plistlib.load(info)
            self.CFBundleIdentifier = pl['CFBundleIdentifier']
        
        print(f'Found CFBundleIdentifier: {self.CFBundleIdentifier}')
        dlg.Destroy()


    def on_select_capabilities(self, event):
        #TODO: Set RUN Button modal disabled unless the previous two buttons are enabled
        #TODO: The RUN button should run something like ./tccplus add CAPABILITY ID_OF_APP
        dlg = CapabilitiesDialog(self)
        dlg.ShowModal()
        self.run_btn.Enable()
        dlg.Destroy()

    def on_run(self, event):
        print(enabled_capabilities)
        for capability in enabled_capabilities:
            print(capability)
            subprocess.Popen(['./tccplus', 'add', capability, self.CFBundleIdentifier], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def on_close(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    frame = MyApp()
    frame.Show()
    app.MainLoop()


