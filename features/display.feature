Feature: Resolution Selection

    Scenario: Set to Kano's preferred resolution
        Given Kano's list of preferred resolutions (defined below)
         When I turn on the screen
         Then the OS detects the screen's preferred mode (CEA or DMT)
          And the OS detects the screen's preferred aspect ratio
          And the OS loads a list of Kano's preferred resolutions for that configuration
          And the OS selects the preferred resolution from that list which the screen supports
          And the OS outputs an HDMI signal with that HDMI mode and resolution

    Scenario: Set to Kano's preferred resolution for 16:9 screens
        Given a screen's aspect ratio is 16:9
         When the OS is searching for Kano's preferred resolutions in the screen's EDID list
         Then it looks for 1366 x 768px
          And then it looks for 1360 x 768px
          And then it looks for 1280 x 720px

    Scenario: Set to Kano's preferred resolution for 16:10 screens
        Given a screen's aspect ratio is 16:10
         When the OS is searching for Kano's preferred resolutions in the screen's EDID list
         Then it looks for 1280 x 800px
          And then it looks for 1440 x 900px

    Scenario: Set to Kano's preferred resolution for 4:3 screens
        Given a screen's aspect ratio is 4:3
         When the OS is searching for Kano's preferred resolutions in the screen's EDID list
         Then it looks for 1280 x 960px
          And then it looks for 1024 x 768px

    Scenario: Turn on a CEA screen with a supported resolution
        Given I have a CEA screen
          And My screen supports one of Kano's preferred CEA resolutions
         When I turn on my kit
         Then I want the OS to output HDMI signal in CEA mode
          And I want that resolution to be the best possible resolution (using Kano's CEA preference list)
          And I want sound to work
          And I don't want the OS to reboot

    Scenario: Turn on a DMT screen with a supported resolution
        Given I have a DMT screen
          And My screen supports one of Kano's preferred DMT resolutions
         When I turn on my kit
         Then I want the OS to output HDMI signal in DMT mode
          And I want that resolution to be the best possible resolution (using Kano's DMT preference list)
          And I want sound to work
          And I don't want the OS to reboot

    Scenario: Turn on a screen without a supported resolution
        Given My screen doesn't support one of Kano's preferred resolutions
         When I turn on my kit
         Then I want the OS to output an HDMI signal with my screen's preferred resolution and mode
          And I want sound to work
          And I don't want the OS to reboot

    Scenario: Turn on a screen without EDID information
        Given My screen doesn't send the OS any EDID information
         When I turn on my kit
         Then I want the OS to output Kano's preferred resolution: 1280x800
          And I want sound to work
          And I don't want the OS to reboot

