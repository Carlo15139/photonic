# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from luxon import g
from luxon import router
from luxon import register
from luxon import render_template
from luxon.utils.bootstrap4 import form

from photonic.models.tenants import luxon_tenant


g.nav_menu.add('/Accounts/Tenants',
               href='/accounts/tenants',
               tag='users:admin',
               feather='paperclip')


@register.resources()
class Tenants():
    def __init__(self):
        router.add('GET',
                   '/accounts/tenants',
                   self.list,
                   tag='tenants:view')

        router.add('GET',
                   '/accounts/tenants/{id}',
                   self.view,
                   tag='tenants:view')

        router.add('GET',
                   '/accounts/tenants/delete/{id}',
                   self.delete,
                   tag='tenants:admin')

        router.add(('GET', 'POST',),
                   '/accounts/tenants/add',
                   self.add,
                   tag='tenants:admin')

        router.add(('GET', 'POST',),
                   '/accounts/tenants/edit/{id}',
                   self.edit,
                   tag='tenants:admin')

    def list(self, req, resp):
        return render_template('photonic/tenants/list.html',
                               view='Tenants')

    def delete(self, req, resp, id):
        tenant = req.context.api.execute('DELETE', '/v1/tenant/%s' % id)

    def view(self, req, resp, id):
        tenant = req.context.api.execute('GET', '/v1/tenant/%s' % id)
        html_form = form(luxon_tenant, tenant.json, readonly=True)
        return render_template('photonic/tenants/view.html',
                               view='View Tenant',
                               form=html_form,
                               id=id)

    def edit(self, req, resp, id):
        if req.method == 'POST':
            req.context.api.execute('PUT', '/v1/tenant/%s' % id, data=req.form_dict)
            return self.view(req, resp, id)
        else:
            tenant = req.context.api.execute('GET', '/v1/tenant/%s' % id)
            html_form = form(luxon_tenant, tenant.json)
            return render_template('photonic/tenants/edit.html',
                                   view='Edit Tenant',
                                   form=html_form,
                                   id=id)

    def add(self, req, resp):
        if req.method == 'POST':
            response = req.context.api.execute('POST', '/v1/tenant', data=req.form_dict)
            return self.view(req, resp, response.json['id'])
        else:
            html_form = form(luxon_tenant)
            return render_template('photonic/tenants/add.html',
                                   view='Add Tenant',
                                   form=html_form)
