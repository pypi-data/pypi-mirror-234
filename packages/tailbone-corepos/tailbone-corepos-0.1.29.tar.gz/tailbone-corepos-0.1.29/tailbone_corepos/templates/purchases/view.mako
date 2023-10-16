## -*- coding: utf-8; -*-
<%inherit file="tailbone:templates/purchases/view.mako" />

<%def name="object_helpers()">
  ${parent.object_helpers()}
  % if master.has_perm('download_for_corepos'):
      <div class="object-helper">
        <h3>Integrations</h3>
        <div class="object-helper-content">
          <corepos-downloader></corepos-downloader>
        </div>
      </div>
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  % if master.has_perm('download_for_corepos'):
      <script type="text/x-template" id="corepos-downloader-template">
        <div>
          <b-button type="is-primary"
                    icon-pack="fas"
                    icon-left="fas fa-download"
                    @click="showDialog = true">
            Download for CORE-POS
          </b-button>
          <b-modal has-modal-card
                   :active.sync="showDialog">
            <div class="modal-card">

              <header class="modal-card-head">
                <p class="modal-card-title">Download Purchase for CORE-POS</p>
              </header>

              <section class="modal-card-body">
                <p class="block">
                  You can download this Purchase as a data file, which can then
                  be imported as a new Purchase Order in CORE Office.
                </p>
              </section>

              <footer class="modal-card-foot">
                <div class="level" style="width: 100%;">
                  <div class="level-left">
                    <div class="level-item buttons">
                      <b-button @click="showDialog = false">
                        Cancel
                      </b-button>
                      <b-button type="is-primary"
                                @click="beginDownload()"
                                icon-pack="fas"
                                icon-left="download">
                        Download for CORE-POS
                      </b-button>
                    </div>
                  </div>
                  % if corepos_import_url:
                      <div class="level-right">
                        <div class="level-item buttons">
                          <b-button type="is-primary"
                                    tag="a" href="${corepos_import_url}" target="_blank"
                                    icon-pack="fas"
                                    icon-left="fas fa-external-link-alt">
                            Go to CORE Office
                          </b-button>
                        </div>
                      </div>
                  % endif
                </div>
              </footer>
            </div>
          </b-modal>
        </div>
      </script>
  % endif
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if master.has_perm('download_for_corepos'):
      <script type="text/javascript">

        let CoreposDownloader = {
            template: '#corepos-downloader-template',
            data() {
                return {
                    showDialog: false,
                }
            },
            methods: {
                beginDownload() {
                    location.href = '${url('{}.download_for_corepos'.format(route_prefix), uuid=instance.uuid)}'
                },
            }
        }

        Vue.component('corepos-downloader', CoreposDownloader)

      </script>
  % endif
</%def>


${parent.body()}
