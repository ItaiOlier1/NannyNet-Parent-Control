import datetime

import wx
import time
from pubsub import pub
import wx.lib.scrolledpanel





class RegistrationPanel(wx.Panel):

    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, style=wx.SIMPLE_BORDER)

        self.frame = frame
        self.parent = parent

        self.SetBackgroundColour(wx.LIGHT_GREY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, -1, label="Register\nNew User")
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.BLACK)
        title.SetFont(titlefont)

        self.action_message = wx.StaticText(self, -1)
        # Set the font and color of the title text
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.BLACK)
        title.SetFont(titlefont)
        self.action_message.Show(False)

        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        nameText = wx.StaticText(self, 1, label="UserName: ")
        self.nameField = wx.TextCtrl(self, -1, name="username", size=(150, -1))
        nameBox.Add(nameText, 0, wx.ALL, 5)
        nameBox.Add(self.nameField, 0, wx.ALL, 5)

        passBox = wx.BoxSizer(wx.HORIZONTAL)
        passText = wx.StaticText(self, 1, label="Password: ")
        self.passField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(150, -1))
        passBox.Add(passText, 0, wx.ALL, 5)
        passBox.Add(self.passField, 0, wx.ALL, 5)

        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.regBtn = wx.Button(self, wx.ID_ANY, label="Register", size=(100, 40))
        btnBox.Add(self.regBtn, 1, wx.ALL, 5)
        self.backBtn = wx.Button(self, wx.ID_ANY, label="Back", size=(100, 40))
        btnBox.Add(self.backBtn, 0, wx.ALL, 5)


        # binds

        self.regBtn.Bind(wx.EVT_BUTTON, self.handle_sign_up)
        self.backBtn.Bind(wx.EVT_BUTTON, self.show_login_panel)

        sizer.Add(title, 0, wx.CENTER | wx.TOP, 5)
        sizer.AddSpacer(10)
        sizer.Add(nameBox, 0, wx.CENTER | wx.ALL, 5)
        sizer.Add(passBox, -1, wx.CENTER | wx.ALL, 5)
        sizer.AddSpacer(10)
        sizer.Add(btnBox, wx.CENTER | wx.ALL, 5)
        sizer.Add(self.action_message, wx.CENTER | wx.ALL, 5)

        pub.subscribe(self.reg_status, "reg_status")


        self.SetSizer(sizer)
        self.Layout()
        self.Hide()


    def reg_status(self, status):
        if status[0] == "True":
            self.parent.change_panel(self,self.parent.home)
        else:
            self.frame.SetStatusText("username already exist")


    def handle_sign_up(self, event):
        username = self.nameField.GetValue()
        password = self.passField.GetValue()
        if not username or not password:
            self.frame.SetStatusText("Must enter name and password")
        else:
            self.frame.logic_q.put(("registration", username, password))



    # Method to show the login panel
    def show_login_panel(self, event):
        self.parent.change_panel(self,self.parent.login)


class HomePanel(wx.Panel):

    def __init__(self, parent, frame):
        super().__init__(parent)

        self.frame = frame
        self.parent = parent

        self.kids_username_list = []

        # First retrieve the screen size of the device
        screenSize = wx.DisplaySize()
        screenWidth = screenSize[0]
        screenHeight = screenSize[1]

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        panel1 = wx.Panel(self, size=(screenWidth, 100), pos=(0, 0), style=wx.SIMPLE_BORDER)

        panel1.SetBackgroundColour('#FFFFFF')

        # logo
        png_logo = wx.Image('picturs/logo.png', wx.BITMAP_TYPE_ANY)
        png_logo = png_logo.Rescale(137, 90).ConvertToBitmap()
        self.bitmap_logo = wx.StaticBitmap(self, -1, png_logo, (png_logo.GetWidth(), png_logo.GetHeight()))

        panel1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel1.SetSizer(panel1_sizer)

        self.add_computerBtn = wx.Button(panel1, label="Add Computer", size=(150, 80))
        self.add_kidBtn = wx.Button(panel1, label="Add Kid", size=(150, 80))

        self.add_computerBtn.Bind(wx.EVT_BUTTON, self.add_new_computer)
        self.add_kidBtn.Bind(wx.EVT_BUTTON, self.add_new_kid)

        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        panel1_text = wx.StaticText(panel1, label="WELCOME BACK")
        panel1_text.SetFont(font)

        panel1_sizer.Add(self.bitmap_logo, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel1_sizer.AddSpacer(20)  # Add a stretch spacer to center the buttons
        panel1_sizer.Add(panel1_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel1_sizer.AddStretchSpacer(1)  # Add a stretch spacer to center the buttons
        panel1_sizer.Add(self.add_computerBtn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel1_sizer.AddSpacer(10)  # Add a stretch spacer to center the buttons
        panel1_sizer.Add(self.add_kidBtn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel1_sizer.AddSpacer(10)  # Add a stretch spacer to center the buttons

        # self.panel2 = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(screenWidth, 350),
        #                                             style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.panel2 = wx.Panel(self, size=(screenWidth, 200), pos=(0, 0), style=wx.SIMPLE_BORDER)
        #self.panel2.SetupScrolling()

        self.panel2.SetBackgroundColour('BFBFBF')
        self.panel2_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scroll = wx.ScrolledWindow(self.panel2, style=wx.VSCROLL)
        self.scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll.SetSizer(self.scroll_sizer)
        self.scroll.SetScrollRate(0, 20)

        self.panel2_sizer.Add(self.scroll, 1, wx.EXPAND | wx.ALL, 10)
        self.panel2.SetSizer(self.panel2_sizer)
        self.Layout()

        self.kid_obj = None
        pub.subscribe(self.parent_computers_status, "parent_computers_status")
        pub.subscribe(self.parent_kids_username_status, "parent_kids_username_status")
        pub.subscribe(self.handle_kid_status, "handle_kid_status")
        pub.subscribe(self.handle_prohibited_addresses_dialog_status, "handle_prohibited_addresses_dialog_status")
        pub.subscribe(self.handle_prohibited_apps_dialog_status, "handle_prohibited_apps_dialog_status")
        pub.subscribe(self.update_remaining_time_status, "update_remaining_time_status")
        #pub.subscribe(self.handle_history_status, "handle_history_status")
        pub.subscribe(self.handle_time_limit_status, "handle_time_limit_status")

        self.panel3 = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1300, 1000),
                                                    style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)

        self.panel3.SetBackgroundColour('#FDDF99')

        self.panel3.SetupScrolling()



        # set the dialogs:
        self.prohibited_addresses_dialog = None
        self.prohibited_apps_dialog = None
        self.history_dialog = None
        self.time_limit_dialog = TimeLimitDialog(self)
        self.prohibited_hours_dialog = None
        self.block_computer_combo_box = None
        self.block_internet_combo_box = None








        self.panel5 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)

        self.panel5.SetBackgroundColour('#FFFFFF')

        # profile picture
        png_profile_pic = wx.Image('picturs/default_profile_pic.png', wx.BITMAP_TYPE_ANY)
        png_profile_pic = png_profile_pic.Rescale(100, 90).ConvertToBitmap()
        self.bitmap_profile_pic = wx.StaticBitmap(self.panel5, -1, png_profile_pic,
                                                  (png_profile_pic.GetWidth(), png_profile_pic.GetHeight()))

        # active picture
        png_active_pic = wx.Image('picturs/active_pic.png', wx.BITMAP_TYPE_ANY)
        png_active_pic = png_active_pic.Rescale(137, 90).ConvertToBitmap()
        self.bitmap_png_active_pic = wx.StaticBitmap(self.panel5, -1, png_active_pic, (png_active_pic.GetWidth(), png_active_pic.GetHeight()))

        font = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.panel5_profile_header = wx.StaticText(self.panel5, label="<Name> Profile")
        self.panel5_profile_header.SetFont(font)

        panel5_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel5_sizer.Add(self.bitmap_profile_pic, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel5_sizer.AddSpacer(10)
        panel5_sizer.Add(self.bitmap_png_active_pic, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        panel5_sizer.AddSpacer(20)  # Add a stretch spacer to center the buttons
        panel5_sizer.Add(self.panel5_profile_header, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.panel5.SetSizer(panel5_sizer)

        self.panel5.Hide()




        self.panel6 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)

        self.panel6.SetBackgroundColour('#D3D3D3')
        self.remaining_time_text = wx.StaticText(self.panel6, label="Time Left")
        self.remaining_time_text.SetFont(font)

        panel6_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel6_sizer.Add(self.remaining_time_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.panel6.SetSizer(panel6_sizer)

        self.panel6.Hide()






        self.panel7 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)
        self.panel7.SetBackgroundColour('#DCDCDC')

        history_button = wx.Button(self.panel7, label="Browsing History", size=(650, 100))
        history_button.Bind(wx.EVT_BUTTON, self.ask_history)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        history_button.SetFont(font)
        history_button.SetBackgroundColour('#007ACC')

        panel7_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel7_sizer.AddStretchSpacer(1)  # Add a flexible spacer to center-align the button
        panel7_sizer.Add(history_button, 0, wx.ALIGN_CENTER)  # Add the button with center alignment
        panel7_sizer.AddStretchSpacer(1)  # Add another flexible spacer to center-align the button
        self.panel7.SetSizer(panel7_sizer)

        self.panel7.Hide()





        self.panel8 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)
        self.panel8.SetBackgroundColour('#DCDCDC')

        time_limit_button = wx.Button(self.panel8, label=" Time Limit", size=(650, 100))
        time_limit_button.Bind(wx.EVT_BUTTON, self.open_time_limit_dialog)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        time_limit_button.SetFont(font)
        time_limit_button.SetBackgroundColour('#007ACC')

        panel8_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel8_sizer.AddStretchSpacer(1)  # Add a flexible spacer to center-align the button
        panel8_sizer.Add(time_limit_button, 0, wx.ALIGN_CENTER)  # Add the button with center alignment
        panel8_sizer.AddStretchSpacer(1)  # Add another flexible spacer to center-align the button
        self.panel8.SetSizer(panel8_sizer)

        self.panel8.Hide()





        self.panel9 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)
        self.panel9.SetBackgroundColour('#DCDCDC')

        prohibited_hours_range_button = wx.Button(self.panel9, label=" Edit Prohibited Hours Ranges", size=(650, 100))
        prohibited_hours_range_button.Bind(wx.EVT_BUTTON, self.ask_prohibited_sets_of_hours)

        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        prohibited_hours_range_button.SetFont(font)
        prohibited_hours_range_button.SetBackgroundColour('#007ACC')

        panel9_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel9_sizer.AddStretchSpacer(1)  # Add a flexible spacer to center-align the button
        panel9_sizer.Add(prohibited_hours_range_button, 0, wx.ALIGN_CENTER)  # Add the button with center alignment
        panel9_sizer.AddStretchSpacer(1)  # Add another flexible spacer to center-align the button
        self.panel9.SetSizer(panel9_sizer)

        self.panel9.Hide()





        self.panel10 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)
        self.panel10.SetBackgroundColour('#DCDCDC')

        prohibited_addresses_button = wx.Button(self.panel10, label=" Edit Prohibited Addresses", size=(650, 100))
        prohibited_addresses_button.Bind(wx.EVT_BUTTON, self.ask_prohibited_addresses)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        prohibited_addresses_button.SetFont(font)
        prohibited_addresses_button.SetBackgroundColour('#007ACC')

        panel10_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel10_sizer.AddStretchSpacer(1)  # Add a flexible spacer to center-align the button
        panel10_sizer.Add(prohibited_addresses_button, 0, wx.ALIGN_CENTER)  # Add the button with center alignment
        panel10_sizer.AddStretchSpacer(1)  # Add another flexible spacer to center-align the button
        self.panel10.SetSizer(panel10_sizer)

        self.panel10.Hide()





        self.panel11 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 100), style=wx.SIMPLE_BORDER)
        self.panel11.SetBackgroundColour('#DCDCDC')

        prohibited_apps_button = wx.Button(self.panel11, label=" Edit Prohibited Applications", size=(650, 100))
        prohibited_apps_button.Bind(wx.EVT_BUTTON, self.ask_prohibited_apps)
        font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        prohibited_apps_button.SetFont(font)
        prohibited_apps_button.SetBackgroundColour('#007ACC')

        panel11_sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel11_sizer.AddStretchSpacer(1)  # Add a flexible spacer to center-align the button
        panel11_sizer.Add(prohibited_apps_button, 0, wx.ALIGN_CENTER)  # Add the button with center alignment
        panel11_sizer.AddStretchSpacer(1)  # Add another flexible spacer to center-align the button
        self.panel11.SetSizer(panel11_sizer)

        self.panel11.Hide()




        self.panel12 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 150), style=wx.SIMPLE_BORDER)
        self.panel12.SetBackgroundColour('#FFFFFF')

        self.panel12_sizer = wx.BoxSizer(wx.VERTICAL)

        #text = wx.StaticText(self.panel12, label='Computer Block', style=wx.ALIGN_CENTER)

        # self.block_computer_bitmap_image = self._toggle_computer_image('picturs/toggle_off_block_computer')  # Create a toggle bitmap with 'toggle_off' image
        # self.toggle_computer_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.toggle_computer_sizer.Add(self.block_computer_bitmap_image)

        # self.block_computer_bitmap_image.Bind(wx.EVT_LEFT_DOWN,
        #                                  self.toggle_computer_click)  # Bind left mouse button click event to toggle_click method
        # print("binding computer")


        # self.panel12_sizer.AddStretchSpacer()  # Add vertical spacer to push the text to the top
        # self.panel12_sizer.Add(text, flag=wx.ALIGN_CENTER)
        # self.panel12_sizer.Add(self.toggle_computer_sizer, flag=wx.ALIGN_CENTER)
        # self.panel12_sizer.AddStretchSpacer()  # Add vertical spacer to push the button to the bottom

        self.panel12.SetSizer(self.panel12_sizer)
        self.panel12.Hide()







        self.panel13 = wx.Panel(self.panel3, size=(self.panel3.GetSize()[0], 150), style=wx.SIMPLE_BORDER)
        self.panel13.SetBackgroundColour('#FFFFFF')

        self.panel13_sizer = wx.BoxSizer(wx.VERTICAL)

        # text = wx.StaticText(self.panel13, label='Internet Block', style=wx.ALIGN_CENTER)

        # self.block_internet_bitmap_image = self._toggle_internet_image('picturs/toggle_off_block_internet')  # Create a toggle bitmap with 'toggle_off' image
        # self.toggle_internet_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.toggle_internet_sizer.Add(self.block_internet_bitmap_image)


        # self.block_internet_bitmap_image.Bind(wx.EVT_LEFT_DOWN,
        #                                  self.toggle_internet_click)  # Bind left mouse button click event to toggle_click method
        # print("binding internet")

        # self.panel13_sizer.AddStretchSpacer()  # Add vertical spacer to push the text to the top
        # self.panel13_sizer.Add(text, flag=wx.ALIGN_CENTER)
        # self.panel13_sizer.Add(self.toggle_internet_sizer, flag=wx.ALIGN_CENTER)
        # self.panel13_sizer.AddStretchSpacer()  # Add vertical spacer to push the button to the bottom

        self.panel13.SetSizer(self.panel13_sizer)
        self.panel13.Hide()






        self.panel3_sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel3_sizer.Add(self.panel5, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel6, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel7, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel8, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel9, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel10, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel11, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel12, 0, wx.EXPAND)
        self.panel3_sizer.Add(self.panel13, 0, wx.EXPAND)


        self.panel3.SetSizer(self.panel3_sizer)
        self.panel3.SetupScrolling()
        self.panel3.Layout()


        self.panel4 = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(600, 1000),
                                                         style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.panel4.SetupScrolling()
        self.panel4.SetBackgroundColour('#FDDF99')

        self.panel4_sizer = wx.BoxSizer(wx.VERTICAL)
        text_label = wx.StaticText(self.panel4, label="Kids")  # Add the text label to self.panel4
        self.panel4_sizer.Add(text_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.panel4_sizer.AddSpacer(50)

        #self.panel4_sizer.AddStretchSpacer()  # Add another stretch spacer to center the buttons vertically
        self.panel4.SetSizer(self.panel4_sizer)



        sizer.Add(self.panel3, 0, wx.ALL | wx.ALIGN_LEFT)
        sizer.Add(self.panel4, 0, wx.ALL | wx.ALIGN_RIGHT)

        main_sizer.Add(panel1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(self.panel2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(sizer, 0)

        self.SetSizer(main_sizer)
        self.Hide()
        self.Layout()
        main_sizer.Layout()

    def ask_prohibited_addresses(self, event):
        username = self.kid_obj.username
        self.frame.logic_q.put(["ask forbidden URLs", username])

    def ask_prohibited_apps(self, event):
        username = self.kid_obj.username
        self.frame.logic_q.put(["ask_forbidden_applications", username])

    def ask_history(self, event):
        self.history_dialog = HistoryDialog(self)
        username = self.kid_obj.username
        pub.subscribe(self.handle_history_status, "handle_history_status")
        self.frame.logic_q.put(["ask_browsing_tracking", username])
        self.history_dialog.ShowModal()
        # self.history_dialog.Destroy()
        # pub.unsubscribe(self.handle_history_status, "handle_history_status")

    def open_time_limit_dialog(self, event):
        self.time_limit_dialog.ShowModal()

    def ask_prohibited_sets_of_hours(self, event):
        self.prohibited_hours_dialog = HoursSetsDialog(self)
        username = self.kid_obj.username
        self.frame.logic_q.put(["ask_forbidden_hours", username])


    def handle_prohibited_addresses_dialog_status(self, status):
        # set the dialogs:
        print(f"statusssss {status}")
        self.prohibited_addresses_dialog = MyDialog(self, "Edit Prohibited Addresses")
        self.prohibited_addresses_dialog.flag_got_first_data = False
        self.prohibited_addresses_dialog.populate_dialog(status)
        self.prohibited_addresses_dialog.ShowModal()
        pub.unsubscribe(self.prohibited_addresses_dialog.on_add_button, "on_add_button")
        pub.unsubscribe(self.prohibited_addresses_dialog.on_delete_button, "on_delete_button")
        self.prohibited_addresses_dialog.Destroy()

    def handle_prohibited_apps_dialog_status(self, status):
        # set the dialogs:
        self.prohibited_apps_dialog = MyDialog(self, "Edit Prohibited Apps")
        self.prohibited_apps_dialog.flag_got_first_data = False
        self.prohibited_apps_dialog.populate_dialog(status)
        self.prohibited_apps_dialog.ShowModal()
        pub.unsubscribe(self.prohibited_apps_dialog.on_add_button, "on_add_button")
        pub.unsubscribe(self.prohibited_apps_dialog.on_delete_button, "on_delete_button")
        self.prohibited_apps_dialog.Destroy()

    def handle_history_status(self, status):
        self.history_dialog.populate_list(status)

    def handle_time_limit_status(self, status):
        self.remaining_time_text.SetLabelText(f"Remaining Time: {status}")
        self.panel6.Layout()


    def _toggle_computer_image(self, bitmap_name):
        print(f"\nbitmap name: {bitmap_name}")
        toggle_bitmap = wx.Bitmap(f'{bitmap_name}.png', wx.BITMAP_TYPE_ANY)  # Load the bitmap image
        image = wx.Bitmap.ConvertToImage(toggle_bitmap)
        image = image.Scale(100, 65)  # Increase size by adding 50 to width and 50 to height
        block_computer_bitmap_image = wx.StaticBitmap(self.panel12, wx.ID_ANY, name=bitmap_name, size=(image.GetWidth(), image.GetHeight()))
        block_computer_bitmap_image.SetBitmap(image.ConvertToBitmap())

        block_computer_bitmap_image.Bind(wx.EVT_LEFT_DOWN,
                                              self.toggle_computer_click)  # Bind left mouse button click event to toggle_click method
        print("binding computer")

        return block_computer_bitmap_image

    def _toggle_internet_image(self, bitmap_name):
        toggle_bitmap = wx.Bitmap(f'{bitmap_name}.png', wx.BITMAP_TYPE_ANY)  # Load the bitmap image
        image = wx.Bitmap.ConvertToImage(toggle_bitmap)
        image = image.Scale(100, 65)  # Increase size by adding 50 to width and 50 to height
        block_internet_bitmap_image = wx.StaticBitmap(self.panel13, wx.ID_ANY, name=bitmap_name, size=(image.GetWidth(), image.GetHeight()))
        block_internet_bitmap_image.SetBitmap(image.ConvertToBitmap())

        block_internet_bitmap_image.Bind(wx.EVT_LEFT_DOWN,
                                              self.toggle_internet_click)  # Bind left mouse button click event to toggle_click method
        print("binding internet")

        return block_internet_bitmap_image


    def toggle_computer_click(self, event):
        username = self.kid_obj.username
        print("clicked")
        toggle = event.GetEventObject().Name  # Get the name of the clicked toggle
        print(f"the toggle is: {toggle} of panel 12")
        if toggle == "picturs/toggle_off_block_computer":
            self.frame.logic_q.put(["block_kid_computer", username])
            toggle_bitmap = self._toggle_computer_image(
                "picturs/toggle_on_block_computer")  # Create a toggle bitmap with 'toggle_on' image
        else:
            self.frame.logic_q.put(["allow_kid_computer", username])
            toggle_bitmap = self._toggle_computer_image(
                "picturs/toggle_off_block_computer")

        self._clear_sizer(self.toggle_computer_sizer)  # Clear the toggle_sizer
        self.toggle_computer_sizer.Add(toggle_bitmap)  # Add the new toggle bitmap to the toggle_sizer
        self.panel12.Layout()

    def toggle_internet_click(self, event):
        print("clicked")
        toggle = event.GetEventObject().Name  # Get the name of the clicked toggle

        if toggle == "picturs/toggle_off_block_internet":
            print(f"the toggle is: {toggle} of panel 13")
            toggle_bitmap = self._toggle_internet_image(
                "picturs/toggle_on_block_internet")  # Create a toggle bitmap with 'toggle_off' image
        else:
            print(f"the toggle is: {toggle} of panel 13")
            toggle_bitmap = self._toggle_internet_image(
                "picturs/toggle_off_block_internet")  # Create a toggle bitmap with 'toggle_off' image

        self._clear_sizer(self.toggle_internet_sizer)  # Clear the toggle_sizer
        self.toggle_internet_sizer.Add(toggle_bitmap)  # Add the new toggle bitmap to the toggle_sizer
        self.panel13.Layout()

    def _clear_sizer(self, sizer):
        for child in sizer.GetChildren():  # Iterate over the children of the sizer
            if child.IsSizer():  # If the child is a sizer
                if child.IsSizer():
                    self._clear_sizer(child.GetSizer())  # Recursively clear the child sizer
            else:
                child.GetWindow().Destroy()  # Destroy the child window
        sizer.Clear()  # Clear the sizer

    def parent_computers_status(self, status):
        print("STATUS-------")
        print(status)
        if status != ['']:
            for mac, nickname in status.items():
                pair_text = f"{mac} - {nickname}"
                #self.pair_label.SetValue(f"{pair_text}\n{self.pair_label.GetValue()}")
                new_text = wx.TextCtrl(self.scroll, value=pair_text, style=wx.TE_READONLY)
                self.scroll_sizer.Add(new_text, 0, wx.EXPAND | wx.ALL, 5)
                self.panel2_sizer.Layout()
                self.scroll_sizer.Layout()
                self.panel2.Layout()


    def parent_kids_username_status(self, status):
        print("STATUS-------usernames####################################################################")
        if type(status) == str:
            status = [status]
        print(status)
        if status != ['']:
            self.kids_username_list.extend(status)
            print(f" kids list: {self.kids_username_list}")
            for username in status:
                self.panel4.SetupScrolling()
                kid_button = wx.Button(self.panel4, label=username, size=(150, 100))
                # bind the new kid's button:
                kid_button.Bind(wx.EVT_BUTTON, self.handle_kids_pressed_button)

                self.panel4_sizer.Add(kid_button, 0, wx.CENTER | wx.ALL, 5)
                self.panel4_sizer.AddSpacer(10)
                self.panel4_sizer.Layout()
                self.panel4.Layout()
        self.panel4.Layout()  # Update the layout of self.panel4

    def handle_kids_pressed_button(self, event):

        print(20*'-' , "in button click")
        kid_username = event.GetEventObject().GetLabel()
        print(f"%%%%%%%{kid_username}")

        print(f"---------------KIDS USERNAMES LIST-------------- {self.kids_username_list}")

        if self.kids_username_list is not None and kid_username in self.kids_username_list:
            # ask the kids data from the server:
            self.frame.logic_q.put(("send parent active to kid", kid_username))


    def handle_kid_status(self, status):
        print("\n\n\n")
        print(status)
        print("\n\n\n")

        self.kid_obj = status
        self.panel5_profile_header.SetLabelText(f"{status.get_username()} profile")

        if self.kid_obj.active == True:
            self.bitmap_png_active_pic.Show()
        else:
            self.bitmap_png_active_pic.Hide()

        self.remaining_time_text.SetLabelText(f"Remaining Time: {status.get_remaining_time()}")

        self.panel5.Layout()
        self.panel6.Layout()
        self.panel7.Layout()
        self.panel8.Layout()
        self.panel9.Layout()
        self.panel10.Layout()
        self.panel11.Layout()

        text = wx.StaticText(self.panel12, label='Computer Block', style=wx.ALIGN_CENTER)

        computer_block = self.kid_obj.kid_blocks_limitations[0]
        print(f"computer_block AAAAAAAAAAAAAA - {computer_block}")
        if computer_block is False:
            self.block_computer_combo_box = MyComboBox(self.panel12, "off")
        else:
            self.block_computer_combo_box = MyComboBox(self.panel12, "on")


        self.toggle_computer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.toggle_computer_sizer.Add(self.block_computer_combo_box)
        self.panel12_sizer.Clear()
        self.panel12_sizer.AddStretchSpacer()  # Add vertical spacer to push the text to the top
        self.panel12_sizer.Add(text, flag=wx.ALIGN_CENTER)
        self.panel12_sizer.Add(self.toggle_computer_sizer, flag=wx.ALIGN_CENTER)
        self.panel12_sizer.AddStretchSpacer()  # Add vertical spacer to push the button to the bottom

        self.panel12.Layout()



        text = wx.StaticText(self.panel13, label='Internet Block', style=wx.ALIGN_CENTER)

        internet_block = self.kid_obj.kid_blocks_limitations[1]
        print(f"internet block BBBBBBBBB - {internet_block}")
        if internet_block is False:
            self.block_internet_combo_box = MyComboBox(self.panel13, "off")
        else:
            self.block_internet_combo_box = MyComboBox(self.panel13, "on")

        self.toggle_internet_sizer = wx.BoxSizer(wx.VERTICAL)
        self.toggle_internet_sizer.Add(self.block_internet_combo_box)
        self.panel13_sizer.Clear()
        self.panel13_sizer.AddStretchSpacer()  # Add vertical spacer to push the text to the top
        self.panel13_sizer.Add(text, flag=wx.ALIGN_CENTER)
        self.panel13_sizer.Add(self.toggle_internet_sizer, flag=wx.ALIGN_CENTER)
        self.panel13_sizer.AddStretchSpacer()  # Add vertical spacer to push the button to the bottom



        self.panel13.Layout()

        self.panel5.Show()
        self.panel6.Show()
        self.panel7.Show()
        self.panel8.Show()
        self.panel9.Show()
        self.panel10.Show()
        self.panel11.Show()
        self.panel12.Show()
        self.panel13.Show()

        self.panel3.SetupScrolling()
        self.panel3.Layout()

    def update_remaining_time_status(self, status):
        self.remaining_time_text.SetLabelText(f"Remaining Time: {status}")
        self.panel5.Layout()
        self.panel3.Layout()

    def add_new_computer(self, event):
        self.dialog = wx.Dialog(self.frame, title="Add new computer")

        nickname_label = wx.StaticText(self.dialog, label="Please enter a nickname for the computer:")
        self.nickname_text = wx.TextCtrl(self.dialog)
        self.nickname_text.SetValue("ENTER HERE...")


        mac_label = wx.StaticText(self.dialog, label="Please enter the MAC address for the computer:")
        self.mac_text = wx.TextCtrl(self.dialog)
        self.mac_text.SetValue("ENTER HERE...")

        add_button = wx.Button(self.dialog, label="Add")


        self.add_new_computer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_new_computer_sizer.Add(nickname_label, 0, wx.ALL, 5)
        self.add_new_computer_sizer.Add(self.nickname_text, 0, wx.EXPAND | wx.ALL, 5)
        self.add_new_computer_sizer.Add(mac_label, 0, wx.ALL, 5)
        self.add_new_computer_sizer.Add(self.mac_text, 0, wx.EXPAND | wx.ALL, 5)
        self.add_new_computer_sizer.Add(add_button, 0, wx.ALL, 5)
        self.add_new_computer_sizer.AddSpacer(20)

        self.dialog.SetSizerAndFit(self.add_new_computer_sizer)

        pub.subscribe(self.add_computer_status, "add_computer_status")

        self.nickname_text.Bind(wx.EVT_TEXT, lambda event: self.nickname_text.SetValue("") if self.nickname_text.GetValue() == "ENTER HERE..." else None)
        self.mac_text.Bind(wx.EVT_TEXT,
                           lambda event: self.mac_text.SetValue(
                               "") if self.mac_text.GetValue() == "ENTER HERE..." else None)

        add_button.Bind(wx.EVT_BUTTON, self.handle_add_new_computer)

        self.dialog.ShowModal()
        self.Layout()


    def add_new_kid(self, event):
        self.add_new_kid_dialog = wx.Dialog(self.frame, title="Add new kid")

        username_label = wx.StaticText(self.add_new_kid_dialog, label="Please enter a username for a kid:")
        self.username_text = wx.TextCtrl(self.add_new_kid_dialog)



        add_button = wx.Button(self.add_new_kid_dialog, label="Add")


        self.error_label = wx.StaticText(self.add_new_kid_dialog, label="The server did not accept your input, try again...")
        self.error_label.Hide()

        self.add_new_kid_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_new_kid_sizer.Add(username_label,  0, wx.ALL, 5)
        self.add_new_kid_sizer.Add(self.username_text, 0, wx.ALL, 5)
        self.add_new_kid_sizer.Add(add_button, 0, wx.ALL, 5)
        self.add_new_kid_sizer.AddSpacer(20)
        self.add_new_kid_dialog.SetSizerAndFit(self.add_new_kid_sizer)

        pub.subscribe(self.add_kid_status, "add_kid_status")

        self.username_text.Bind(wx.EVT_TEXT,
                                lambda event: self.username_text.SetValue("")
                                        if self.username_text.GetValue() == "" else None)


        add_button.Bind(wx.EVT_BUTTON, self.handle_add_new_kid)

        self.add_new_kid_dialog.ShowModal()
        self.Layout()





    def on_logout(self, event):
        # TODO: implement logout logic here
        print('Logging out...')

    def handle_add_new_computer(self, event):
        nickname = self.nickname_text.GetValue()
        mac_address = self.mac_text.GetValue()

        if not nickname or not mac_address:
            wx.MessageBox("Input is required, try again...", 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            self.frame.logic_q.put(("add new computer", mac_address, nickname))
            print("put")

    def handle_add_new_kid(self, event):
        username = self.username_text.GetValue()

        if not username:
            wx.MessageBox("Input is required, try again...", 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            self.frame.logic_q.put(("add new kid", username))
            print("put")


    def add_computer_status(self, status):
        print("\nhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        if status[0] == "False":
            print("SHOW ERROR")
            wx.MessageBox("The server did not accept your input, try again...", 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("The server happily accepted your input", "Info", wx.OK | wx.ICON_INFORMATION)
            #self.parent_computers_status({str(mac_address): str(nickname)})
            self.parent_computers_status({str(self.mac_text.GetValue()): str(self.nickname_text.GetValue())})

        self.dialog.Layout()
        #wx.CallAfter(self.EndModal, wx.ID_OK)


    def add_kid_status(self, status):
        print("\nhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        if status[0] == "False":
            print("SHOW ERROR")
            wx.MessageBox("The server did not accept your input, try again...", 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("The server happily accepted your input", "Info", wx.OK | wx.ICON_INFORMATION)
            #self.parent_computers_status({str(mac_address): str(nickname)})
            self.parent_kids_username_status([str(self.username_text.GetValue())])

        self.add_new_kid_dialog.Layout()
        #wx.CallAfter(self.EndModal, wx.ID_OK)]


class MyComboBox(wx.ComboBox):
    def __init__(self, parent, initial_selection=None):
        super().__init__(parent, choices=['On', 'Off'], style=wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_selection)

        if initial_selection:
            self.set_selection_by_string(initial_selection)

    def on_combo_selection(self, event):
        selected_value = self.GetStringSelection()
        print(f'Selected: {selected_value}')

    def set_selection_by_string(self, value):
        if value.lower() == 'on':
            self.SetSelection(0)
        elif value.lower() == 'off':
            self.SetSelection(1)


class HoursSetsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(None, title="Select prohibited sets of hours")

        self.choices = []
        self.parent = parent

        for hour in range(0, 24):
            start_time = f"{hour:02d}:00"
            end_time = f"{hour:02d}:59"
            hour_range = f"{start_time} - {end_time}"
            self.choices.append(hour_range)

        self.checkList = wx.CheckListBox(self, choices=self.choices)

        self.__do_layout()

        self.Bind(wx.EVT_CHECKLISTBOX, self.on_check, self.checkList)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        pub.subscribe(self.handle_sets_of_hours_status, "handle_sets_of_hours_status")
        pub.subscribe(self.handle_add_set_of_hours_status, "handle_add_set_of_hours_status")
        pub.subscribe(self.handle_delete_set_of_hours_status, "handle_delete_set_of_hours_status")

    def __do_layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.checkList, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)
        self.Fit()

    def on_check(self, event):
        selected_index = event.GetSelection()
        selected_choice = self.choices[selected_index]

        username = self.parent.kid_obj.username
        if self.checkList.IsChecked(selected_index):
            print(f"{selected_choice} selected")
            self.parent.frame.logic_q.put(["add_set_of_forbidden_hours_to_server", username, selected_choice])
        else:
            print(f"{selected_choice} unselected")
            self.parent.frame.logic_q.put(["delete_set_of_forbidden_hours_to_server", username, selected_choice])

    def handle_sets_of_hours_status(self, status):
        print(f"status: {status}")
        if status is not '':
            if ',' in status:
                status = status.split(',')
            else:
                status = [status]

            # Iterate through the server data and mark the corresponding items in the CheckListBox
            for item in status:
                index = self.checkList.FindString(item)
                if index != wx.NOT_FOUND:
                    self.checkList.Check(index)
            self.Layout()

        self.ShowModal()

    def handle_add_set_of_hours_status(self, status):
        pass

    def handle_delete_set_of_hours_status(self, status):
        pass

    def on_close(self, event):
        pub.unsubscribe(self, "handle_sets_of_hours_status")
        pub.unsubscribe(self, "handle_add_set_of_hours_status")
        pub.unsubscribe(self, "handle_delete_set_of_hours_status")
        self.Destroy()



class TimeLimitDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(None, wx.ID_ANY)

        self.parent = parent

        self.SetTitle("Time Limit")
        self.SetSize((320, 260))

        self.spnHrs = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=23)
        self.spnMin = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=59)
        self.spnSec = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=59)
        self.btnSave = wx.Button(self, wx.ID_ANY, "Save")

        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.Save_OnClick, self.btnSave)


    def __do_layout(self):
        szrHrs = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Hrs:"), wx.HORIZONTAL)
        szrMin = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Min:"), wx.HORIZONTAL)
        szrSec = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Sec:"), wx.HORIZONTAL)

        szrHrs.Add(self.spnHrs, 0, wx.EXPAND, 0)
        szrMin.Add(self.spnMin, 0, wx.EXPAND, 0)
        szrSec.Add(self.spnSec, 0, wx.EXPAND, 0)

        # Save Button
        szrButtons = wx.BoxSizer(wx.HORIZONTAL)
        szrButtons.Add(self.btnSave, 1, wx.EXPAND, 0)

        # Main
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrMain.Add(szrHrs, 0, wx.EXPAND, 0)
        szrMain.Add(szrMin, 0, wx.EXPAND, 0)
        szrMain.Add(szrSec, 0, wx.EXPAND, 0)
        szrMain.Add(szrButtons, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(szrMain)
        self.Layout()

    def Save_OnClick(self, event):
        """Save the entered time limit"""
        hh = self.spnHrs.GetValue()
        mm = self.spnMin.GetValue()
        ss = self.spnSec.GetValue()
        time_limit = datetime.time(hh, mm, ss)
        print("Time Limit:", time_limit.strftime("%H:%M:%S"))
        event.Skip()

        username = self.parent.kid_obj.username
        self.parent.frame.logic_q.put(["send_new_time_limitation", username, time_limit])






class HistoryDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Browsing Tracking List", size=(400, 300))

        self.panel = wx.Panel(self)
        self.parent = parent

        # Header
        header_font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.header = wx.StaticText(self.panel, label="Browsing Tracking List")
        self.header.SetFont(header_font)

        # ListCtrl widget
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.InsertColumn(0, "History Browsing Tracking")

        # Set column widths
        column_widths = [150, 60, 120]  # Set the desired column widths

        for column, width in enumerate(column_widths):
            self.list_ctrl.SetColumnWidth(column, width)

        # Refresh button
        self.refresh_button = wx.Button(self.panel, label="Refresh")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.header, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.refresh_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.panel.SetSizer(sizer)

    def populate_list(self, list):
        self.list_ctrl.DeleteAllItems()
        for row, name in enumerate(list):
            if name != '':
                self.list_ctrl.InsertItem(row, name)



    def on_refresh(self, event):
        username = self.parent.kid_obj.username
        self.parent.frame.logic_q.put(["ask_browsing_tracking", username])

    def on_close(self, event):
        pub.unsubscribe(self, "handle_history_status")
        self.Destroy()



class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title)

        self.parent = parent
        self.title = title
        self.username = self.parent.kid_obj.username
        self.flag_got_first_data = False

        # Main sizer for the dialog
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Text above the input box
        if self.title == "Edit Prohibited Addresses":
            text_label = wx.StaticText(self, label="Please enter a NEW Prohibited Address to Block")
        elif self.title == "Edit Prohibited Apps":
            text_label = wx.StaticText(self, label="Please enter a NEW Prohibited app to Block")
        else:
            text_label = wx.StaticText(self, label="Please enter a Text")
        self.main_sizer.Add(text_label, 0, wx.ALL | wx.EXPAND, 5)

        # Create a scrolled window
        self.scrolled_window = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scrolled_window.SetScrollRate(10, 10)

        # Vertical sizer for text objects
        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        # Set the vertical sizer as the sizer for the scrolled window
        self.scrolled_window.SetSizer(self.vertical_sizer)

        # Input box for new text objects
        self.text_ctrl = wx.TextCtrl(self)
        self.main_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Add button to add new text objects
        self.add_button = wx.Button(self, label="Add")
        self.add_button.Bind(wx.EVT_BUTTON, self.add_request)
        self.main_sizer.Add(self.add_button, 0, wx.ALL, 5)

        # Add the scrolled window to the main sizer
        self.main_sizer.Add(self.scrolled_window, 1, wx.EXPAND | wx.ALL, 5)


        # Set the main sizer for the dialog
        self.SetSizer(self.main_sizer)

        # Store the text objects and delete buttons
        self.text_objects = []
        self.delete_buttons = []

        # pub.subscribe(self.on_add_button, "on_add_button")
        # pub.subscribe(self.on_delete_button, "on_delete_button")

        self.last_button_to_delete_data = None

    def add_request(self, event):
        text = self.text_ctrl.GetValue()
        username = self.username
        if self.title == "Edit Prohibited Addresses":
            self.parent.frame.logic_q.put(["add_new_forbidden_address_to_server", username, text])
        elif self.title == "Edit Prohibited Apps":
            self.parent.frame.logic_q.put(["add_new_forbidden_app_to_server", username, text])


    def delete_request(self, event, horizontal_sizer, text_object, delete_button):
        self.last_button_to_delete_data = horizontal_sizer, text_object, delete_button
        username = self.username
        text = text_object.GetLabel()
        if self.title == "Edit Prohibited Addresses":
            self.parent.frame.logic_q.put(["delete_forbidden_address_to_server", username, text])
        elif self.title == "Edit Prohibited Apps":
            self.parent.frame.logic_q.put(["delete_forbidden_app_to_server", username, text])

    def on_add_button(self, status):
        text = status
        print(f"\n\n{text}")
        print("title " + self.title)
        if text is not None and text is not '':
            # Create a horizontal sizer for each text object and delete button
            horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # Text object
            text_object = wx.StaticText(self.scrolled_window, label=text)
            horizontal_sizer.Add(text_object, 0, wx.ALL, 5)

            # Spacer item to push the delete button to the right side
            horizontal_sizer.Add((1, 1), proportion=1)

            # Delete button for the text object
            delete_button = wx.Button(self.scrolled_window, label="Delete")
            delete_button.Bind(wx.EVT_BUTTON, lambda event, hs=horizontal_sizer, to=text_object, db=delete_button: self.delete_request(event, hs, to, db))
            horizontal_sizer.Add(delete_button, 0, wx.ALL, 5)

            # Add the horizontal sizer to the vertical sizer in the scrolled window
            self.vertical_sizer.Add(horizontal_sizer, 0, wx.EXPAND)

            # Refresh the layout of the vertical sizer in the scrolled window
            self.vertical_sizer.Layout()

            # Fit the scrolled window to update the scrolling area
            self.scrolled_window.FitInside()

            # Append the text object and delete button to the lists
            self.text_objects.append(text_object)
            self.delete_buttons.append(delete_button)

            # Clear the input box
            self.text_ctrl.Clear()

    def on_delete_button(self, status):
        # Retrieve the parent of the horizontal sizer from the scrolled window
        #parent_sizer = self.scrolled_window.GetSizer()
        parent_sizer = self.vertical_sizer
        # Remove the horizontal sizer from its parent sizer
        parent_sizer.Remove(self.last_button_to_delete_data[0])

        # Destroy the delete button and the text object
        self.last_button_to_delete_data[2].Destroy()
        self.last_button_to_delete_data[1].Destroy()

        # Refresh the layout of the vertical sizer
        self.vertical_sizer.Layout()

        # Fit the scrolled window to update the scrolling area
        self.scrolled_window.FitInside()

    def populate_dialog(self, text_list_str):
        if ',' in text_list_str:
            text_list = text_list_str.split(',')
        else:
            text_list = [text_list_str]
        for text in text_list:
            # Create a horizontal sizer for each text object and delete button
            horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # Text object
            text_object = wx.StaticText(self.scrolled_window, label=text)
            horizontal_sizer.Add(text_object, 0, wx.ALL, 5)

            # Spacer item to push the delete button to the right side
            horizontal_sizer.Add((1, 1), proportion=1)

            # Delete button for the text object
            delete_button = wx.Button(self.scrolled_window, label="Delete")
            delete_button.Bind(wx.EVT_BUTTON, lambda event, hs=horizontal_sizer, to=text_object, db=delete_button: self.delete_request(event, hs, to, db))
            horizontal_sizer.Add(delete_button, 0, wx.ALL, 5)

            # Add the horizontal sizer to the vertical sizer in the scrolled window
            self.vertical_sizer.Add(horizontal_sizer, 0, wx.EXPAND)

            # Append the text object and delete button to the lists
            self.text_objects.append(text_object)
            self.delete_buttons.append(delete_button)

        # Refresh the layout of the vertical sizer in the scrolled window
        self.vertical_sizer.Layout()

        # Fit the scrolled window to update the scrolling area
        self.scrolled_window.FitInside()

        self.flag_got_first_data = True
        print(f"text_list: {text_list}")

        pub.subscribe(self.on_add_button, "on_add_button")
        pub.subscribe(self.on_delete_button, "on_delete_button")




# Define the LoginPanel class, which is a subclass of wx.Panel
class LoginPanel(wx.Panel):

    # Constructor for the LoginPanel class
    def __init__(self, parent, frame):
        # Call the constructor of the wx.Panel class and set the position, size, and border style of the panel
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition, style=wx.SIMPLE_BORDER)

        # Set the frame and parent attributes of the LoginPanel object
        self.frame = frame
        self.parent = parent

        # Set the background color of the panel
        self.SetBackgroundColour(wx.LIGHT_GREY)

        # Create a vertical box sizer to organize the elements in the panel
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a title for the login panel using a static text control
        title = wx.StaticText(self, -1, label="Welcome\nLogin")
        # Set the font and color of the title text
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.BLACK)
        title.SetFont(titlefont)

        self.action_message = wx.StaticText(self, -1)
        # Set the font and color of the title text
        titlefont = wx.Font(22, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        title.SetForegroundColour(wx.BLACK)
        title.SetFont(titlefont)
        self.action_message.Show(False)

        # Create a horizontal box sizer for the username field
        nameBox = wx.BoxSizer(wx.HORIZONTAL)
        # Create a label for the username field using a static text control
        nameText = wx.StaticText(self, 1, label="UserName: ")
        # Create a text field for the username using a text control
        self.nameField = wx.TextCtrl(self, -1, name="username", size=(150, -1))
        # Add the label and text field to the horizontal sizer
        nameBox.Add(nameText, 0, wx.ALL, 5)
        nameBox.Add(self.nameField, 0, wx.ALL, 5)

        # Create a horizontal box sizer for the password field
        passBox = wx.BoxSizer(wx.HORIZONTAL)
        # Create a label for the password field using a static text control
        passText = wx.StaticText(self, 1, label="Password: ")
        # Create a text field for the password using a text control with the password style
        self.passField = wx.TextCtrl(self, -1, name="password", style=wx.TE_PASSWORD, size=(150, -1))
        # Add the label and text field to the horizontal sizer
        passBox.Add(passText, 0, wx.ALL, 5)
        passBox.Add(self.passField, 0, wx.ALL, 5)

        # Create a horizontal box sizer for the login and registration buttons
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        # Create a login button using a wx.Button object and bind it to the handle_login method
        self.loginBtn = wx.Button(self, wx.ID_ANY, label="login", size=(100, 40))
        # Add the login button to the horizontal sizer
        btnBox.Add(self.loginBtn, 0, wx.ALL, 5)
        # Create a registration button using a wx.Button object and bind it to the handle_reg method
        self.regBtn = wx.Button(self, wx.ID_ANY, label="Registration", size=(100, 40))
        # Add the registration button to the horizontal sizer
        btnBox.Add(self.regBtn, 1, wx.ALL, 5)

        self.loginBtn.Bind(wx.EVT_BUTTON, self.handle_login)
        self.regBtn.Bind(wx.EVT_BUTTON, self.show_registration_panel)

        # add all elements to sizer
        sizer.Add(title, 0, wx.CENTER | wx.TOP, 5)
        sizer.AddSpacer(10)
        sizer.Add(nameBox, 0, wx.CENTER | wx.ALL, 5)
        sizer.Add(passBox, -1, wx.CENTER | wx.ALL, 5)
        sizer.AddSpacer(10)
        sizer.Add(btnBox, wx.CENTER | wx.ALL, 5)
        #sizer.Add(self.action_message, wx.CENTER | wx.ALL, 5)


        pub.subscribe(self.login_status, "login_status")


        # arrange the screen
        self.SetSizer(sizer)
        self.Layout()
        self.Hide()


    def handle_login(self, event):
        username = self.nameField.GetValue()
        password = self.passField.GetValue()
        if not username or not password:
            self.frame.SetStatusText("Must enter name and password")
        else:
            self.frame.logic_q.put(("login", username,password))


    def login_status(self, status):
       if status[0] == 'True':
           self.parent.change_panel(self,self.parent.home)
       else:
           self.frame.SetStatusText("eerror in username or password")


    def show_registration_panel(self, event):
        self.parent.change_panel(self,self.parent.registration)






class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent)


        self.SetBackgroundColour(wx.WHITE)

        self.frame = parent

        self.v_box = wx.BoxSizer(wx.VERTICAL)



        # create object for each panel
        self.login = LoginPanel(self,self.frame)
        self.registration = RegistrationPanel(self,self.frame)
        self.home = HomePanel(self,self.frame)


        # Add each panel to the vertical box sizer
        self.v_box.Add(self.login,1,wx.EXPAND)
        self.v_box.Add(self.registration,1,wx.EXPAND)
        self.v_box.Add(self.home,1,wx.EXPAND)

        self.login.Show()

        self.SetSizer(self.v_box)
        self.Layout()


    def change_panel(self,oldScr,newScr):
        if newScr is self.home:
            self.frame.logic_q.put("get parent's computers")
            self.frame.logic_q.put("get kids username")

        oldScr.Hide()
        newScr.Show()
        self.SetSizer(self.v_box)
        self.Layout()




class MyFrame(wx.Frame):
    def __init__(self, logic_q, parent=None):
        super(MyFrame, self).__init__(parent,title="Itai project")

        self.SetBackgroundColour(wx.WHITE)

        # create status bar
        self.CreateStatusBar(1)
        self.SetStatusText("Developed by Itay")

        self.Maximize(True)
        self.logic_q = logic_q

        # create main pannel
        main_panel = MainPanel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(main_panel, 1, wx.EXPAND)

        self.SetSizer(box)
        self.Layout()
        self.Show()






if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()





