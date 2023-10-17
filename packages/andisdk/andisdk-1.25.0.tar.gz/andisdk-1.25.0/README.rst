andisdk - ANDi SDK
==================

ANDi SDK is a package to support powerful ANDi scripting API from python environment providing powerful Ethernet and automotive testing development kit.

Calling andisdk from Python
---------------------------

ANDi SDK allows the creation and handling of Ethernet based messages or channels, this can be done with or without an ANDi test project

.. code-block:: python

    # creating a message using a project
    from andisdk import load_project
    api = load_project(path_to_atp)
    eth_msg = api.message_builder.create_ethernet_message()
    # creating a message without a project
    from andisdk import message_builder
    msg = message_builder.create_ethernet_message()


Requirements to run ANDi SDK
----------------------------

ANDi SDK is portable, it can be used on both Windows and Linux machines.  

Before running ANDi SDK, the following requirements need to be met:

- .NET 5 runtime: responsible for running ANDi library files (dlls).  
- CodeMeter: responsible for license handling.  
- Npcap or Winpcap(Windows): responsible for hardware interfaces.  
- Libpcap (Linux): responsible for hardware interfaces.  

Example
-------

.. code-block:: python

    # this example will create and send an udp message
    from andisdk import message_builder, andi
    import sys

    adapters = andi.get_adapters()

    if (len(adapters) <= 0):
        print("No adapters found, stopping script")
        sys.exit()  

    adapter = adapters[0]
    print("using adapter " + adapter.id + " to send udp message")
    channel = andi.create_channel("Ethernet")
    message = message_builder.create_udp_message(channel, channel)

    message.payload = tuple([0x01, 0x02, 0x03, 0x04])
    message.udp_header.port_source = 1234

    print("sending udp message with payload " + str([x for x in message.payload]))
    message.send()

Copyrights and licensing
------------------------

This product is the property of Technica Engineering GmbH.
© Copyright 2022, Technica Engineering GmbH

This product will not function without a proper license.
A proper license can be acquired by contacting Technica Engineering GmbH.
For license related inquiries, this email: support@technica-engineering.de is available from Technica Engineering.
