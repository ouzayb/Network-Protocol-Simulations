# Network-Protocol-Simulations

How to use:
1. Open "main.py" file.
2. Select the desired version to use from the dropdown menu.
3. from the right, select the desired effect on the package or the ack and press the "Send Instructions" button.
4. Wait until the process is done and click the button again after selecting different scenerios. 
(if none of the checkboxes are selected, it will perfectly without any packages being lost, late or corrupted)

IMPORTANT NOTES FROM THE DEVELOPER:
* The effects are applied when sending the package leaves the protocol for the unreliable channel. If the 
selections are not cleared, they will continue to be in affect until the checkboxes are cleared even in the same
simulation.

For example in RDT2.0 if you select corrupt package, it will continue to send corrupt packages EVEN THOUGH 
the "Send Instructions" button is disabled. After sending the corrupt package, 
~~THE CHECKBOX SHOULD BE UNCHECKED BEFORE THE NEXT PACKAGE IS SENT~~ to send an uncorrupted 
package or the next package will be corrupted as well and it will continuosly send corrupted packages.


Coded by:
Ouzayb