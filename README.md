# TccPylus

Manage your apps permissions on macOS while keeping AMFI and SIP disabled

# Why this app?

Many OpenCore Legacy Patcher users may have encountered a typical issue of having AMFI and SIP disabled: most of the apps that require special permissions such as Microphone and Camera, don't work and there's no way apparently to fix it.

Luckily there's a way which consists of using the terminal with a script called tccplus, but it's not much user friendly in my opinion.

# Usage

1. Click on `Select App` and select the app you want modify the permissions
2. Click on `Select Capabilities` and check the capabilities you wanna add (e.g. `Microphone`, `Camera` etc)
3. Click on `Run` and you should be good to go

Just as a double-check, open `System Settings` application, under `Privacy & Security` -> open the desired capability (e.g. `Camera`) and check if the app is present.


# Roadmap

- [ ] If SIP is enabled, display an error message with some suggestions (e.g. `csrutil disable` or tweak `csr-active-config` accordingly)
- [ ] If AMFI is not disabled using `amfi_get_out_of_my_way=0x1` boot-arg, display an error message with the proper suggestion
- [ ] Improve the GUI quality with some images or something like that ._.
- [ ] Implement using GitHub Action the building of the `.app` using `py2app`
- [ ] Use a custom `Info.plist` which will be parsed by `py2app` using GitHub Action

# Credits

- [wxPython](https://github.com/wxWidgets/Phoenix) for the GUI
- [ronaldoussoren](https://github.com/ronaldoussoren/py2app) for [py2app](https://github.com/ronaldoussoren/py2app) to build a standalone `.app` application
- [jslegendre](https://github.com/jslegendre) for [tccplus](https://github.com/jslegendre/tccplus)
- [ChatGPT](https://chat.openai.com) because it was 4AM and I was too lazy to code properly haha