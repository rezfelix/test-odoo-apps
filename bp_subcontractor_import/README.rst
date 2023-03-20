===================================
Subcontractor Serial Numbers Import
===================================

This module extends the functionality of stock module to allow import serial numbers for Subcontractors
from an excel or CSV file.

Configuration
=============

To configure this module, you need to:

#. the routes of the finish product should be Buy/Resupply Subcontractor on Order.
#. the routes of the components should be Replenish on Order (MTO)/Buy/Dropship Subcontractor on Order.
#. Make sure that the Tracking is By Unique Serial Number/ or By Lots.
#. Make sure that at least on vendor in the the components.
#. Go to a *Manufacture > *Bills of Materials*.
#. Create a bill of Material with the products supposed to be imported from the file.
#. assign the partner to the subcontractors.

Usage
=====

To use this module you need to:

#. Go to create and confirm a purchase order with subcontractor partner for the finish product.
#. Go to Receipt and Click on Icon from the Operations for the Finish product.
#. Select an excel file.
#. Choose the search will be by Name or default code.
#. Click on import button.
#. Confirm the delivery and check the Traceability.
