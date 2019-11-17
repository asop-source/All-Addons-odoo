# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2019 vitraining.com.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Pengajuan Dana dan Reimberse",
    "version": "0.1",
    "author": "vitraining.com",
    "category": "Extra Tools",
    "website": "www.vitraining.com",
    "license": "AGPL-3",
    "summary": "",
    "description": """
   * Ajuan dana (Uang Untuk Dipertanggungjawabkan/UUDP)
   * Reimbersement
   * Pencairan dana / reimberse
   * Penyelesaian / pertanggungjawaban dana
   * Tidak ada jurnal terkait bank / cash
""",
    "depends": ["analytic",
                "account",
                "hr",
                "product",
                "purchase",
                "sale",
                "hr_expense",],
    "data":[
        "security/uudp_sequence.xml",
        "security/ir.model.access.csv",
        "security/group.xml",
        "views/uudp.xml",
        "views/product.xml",
        "views/partner.xml",
        "data/data.xml",
        ],
    "demo": [],
    "qweb": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "application": True,
}