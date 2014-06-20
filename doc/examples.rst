********
Examples
********


Management
==========

List technologies
~~~~~~~~~~~~~~~~~

The following code block will display each :term:`technology` available on
your system:

.. code-block:: python

	import pyconnman

    technologies = manager.get_technologies()
    print '========================================================='
    for i in technologies:
        (path, params) = i
        print path, '['+params['Name']+']'

**Example output:**

.. code-block:: python

    =========================================================
    /net/connman/technology/bluetooth [Bluetooth]
    /net/connman/technology/wifi [WiFi]
    /net/connman/technology/ethernet [Wired]


List services
~~~~~~~~~~~~~

The following code block will display each :term:`service` available on
your system:

.. code-block:: python

    services = manager.get_services()
    print '========================================================='
    for i in services:
        (path, params) = i
        print path, '['+params['Name']+']'

**Example output:**

.. code-block:: python

    =========================================================
    /net/connman/service/ethernet_b827ebaf24d8_cable [Wired]
    /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk [BTHub5-NG6W]
    /net/connman/service/wifi_000f1330203f_4254576946692d776974682d464f4e_managed_none [BTWiFi-with-FON]
    /net/connman/service/wifi_000f1330203f_544e434150374345434535_managed_psk [TNCAP7CECE5]
    /net/connman/service/wifi_000f1330203f_4449524543542d376b5b54565d55453430455337303030_managed_psk [DIRECT-7k[TV]UE40ES7000]
    /net/connman/service/wifi_000f1330203f_534b593344463746_managed_psk [SKY3DF7F]
    /net/connman/service/wifi_000f1330203f_45452d427269676874426f782d717862363236_managed_psk [EE-BrightBox-qxb626]
