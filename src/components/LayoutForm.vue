<script>
import moment from 'moment';
import {
  DEFAULT_TAGS,
  DEFAULT_EINHEITEN,
  DEFAULT_ORT,
  STICHWORT_OPTIONS,
  DAUER_OPTIONS,
  ORT_OPTIONS,
  EINHEITEN_OPTIONS,
  BERICHT_OPTIONS,
  TAG_OPTIONS
} from '../config.js';

export default {
  components: {},
  data() {
    return {
      started: false,
      nummer: '',
      datum: '',
      jahr: '',
      uhrzeit: '',
      dauer: '',
      stichwort: '',
      ort: DEFAULT_ORT,
      einheiten: DEFAULT_EINHEITEN,
      bericht: '',
      tags: DEFAULT_TAGS,
      link: '',
      // Expose config options to template
      stichwortOptions: STICHWORT_OPTIONS,
      dauerOptions: DAUER_OPTIONS,
      ortOptions: ORT_OPTIONS,
      einheitenOptions: EINHEITEN_OPTIONS,
      berichtOptions: BERICHT_OPTIONS,
      tagOptions: TAG_OPTIONS,
      toastMessage: '',
      showToastNotification: false,
      toastTimeoutId: null
    }
  },
  watch: {
    datum(newDateValue) {
      if (newDateValue) {
        const m = moment(newDateValue, "YYYY-MM-DD");

        if (m.isValid()) {
          this.jahr = m.year();
        } else {
          this.jahr = '';
        }
      } else {
        this.jahr = '';
      }
    }
  },
  methods: {
    format_date(value) {
      if (value) {
        return moment(String(value)).format('DD.MM.YYYY')
      }
    },
    set_stichwort(val) {
      this.stichwort = val;
    },
    set_heute() {
      const now = moment();
      this.datum = now.format("YYYY-MM-DD");
      this.uhrzeit = now.format("HH:mm");
    },
    set_gestern() {
      const yesterday = moment().subtract(1, "days");
      this.datum = yesterday.format("YYYY-MM-DD");
      this.uhrzeit = moment().format("HH:mm");
    },
    set_dauer(val) {
      this.dauer = val;
    },
    set_ort(val) {
      this.ort = val + ", ";
    },
    set_einheiten(val) {
      if (this.einheiten.length == 0) {
        this.einheiten = val;
      } else {
        this.einheiten = `${this.einheiten}, ${val}`;
      }
    },
    set_bericht(val) {
      this.bericht = val;
    },
    set_tags(val) {
      this.tags = `${this.tags} ${val}`;
    },
    reset_einheiten() {
      this.einheiten = DEFAULT_EINHEITEN;
    },
    reset_einsatzbericht() {
      this.bericht = "";
    },
    reset_tags() {
      this.tags = DEFAULT_TAGS;
    },
    create_example() {
      const now = moment();
      this.nummer = "42";
      this.datum = now.startOf('month').format("YYYY-MM-DD");
      this.jahr = now.format("YYYY");
      this.uhrzeit = now.format("HH:mm");
      this.dauer = "1 Stunde";
      this.stichwort = "TMR-1 Türnotöffnung";
      this.ort = `${DEFAULT_ORT}, Bertolt-Brecht-Straße 18`;
      this.einheiten = `${DEFAULT_EINHEITEN}, Rettungsdienst, Polizei`;
      this.bericht = 'Das ist ein Beispiel Einsatzbericht.';
      this.tags = DEFAULT_TAGS;
      this.link = 'https://www.feuerwehr-werdau.de/';
    },
    clear_form() {
      this.nummer = '';
      this.datum = '';
      this.jahr = '';
      this.uhrzeit = '';
      this.dauer = '';
      this.stichwort = '';
      this.ort = DEFAULT_ORT;
      this.einheiten = DEFAULT_EINHEITEN;
      this.bericht = '';
      this.tags = DEFAULT_TAGS;
      this.link = '';
    },
    showToast(message) {
      this.toastMessage = message;
      this.showToastNotification = true;

      if (this.toastTimeoutId) {
        clearTimeout(this.toastTimeoutId);
      }

      this.toastTimeoutId = setTimeout(() => {
        this.showToastNotification = false;
        this.toastTimeoutId = null;
      }, 3000);
    },
    async copyText(mode) {
      const el = this.$refs.vorschauContent;

      // Clone node to manipulate it without affecting view
      const clone = el.cloneNode(true);

      // Handle Instagram specific logic
      if (mode === 'instagram') {
        clone.querySelectorAll('.hide-on-instagram').forEach(e => e.remove());
        clone.querySelectorAll('.show-only-on-instagram').forEach(e => e.style.display = 'block');
      } else {
        clone.querySelectorAll('.show-only-on-instagram').forEach(e => e.remove());
      }

      // Temporarily append to DOM to ensure innerText works consistently
      clone.style.position = 'absolute';
      clone.style.left = '-9999px';
      document.body.appendChild(clone);

      const text = clone.innerText;

      try {
        await navigator.clipboard.writeText(text);
        this.showToast(mode === 'instagram' ? 'Text für Instagram kopiert!' : 'Text kopiert!');
      } catch (err) {
        console.error('Failed to copy: ', err);
        this.showToast('Fehler beim Kopieren.');
      } finally {
        document.body.removeChild(clone);
      }
    }
  },
  beforeUnmount() {
    if (this.toastTimeoutId) {
      clearTimeout(this.toastTimeoutId);
    }
  }
};
</script>

<template>
  <div class="columns is-multiline">
    <!-- Toast Notification -->
    <div class="toast-notification notification is-primary" v-if="showToastNotification">
      {{ toastMessage }}
    </div>

    <div class="column is-12">
      <h3 class="title is-4">Einsatzdaten eingeben <span class="tag is-primary is-clickable" @click="create_example">Beispiel generieren</span></h3>

      <div class="grid">
        <div class="cell is-col-start-1">
          <label for="nummer" class="label">Nummer <span class="tag is-primary is-clickable" @click="nummer++">+1</span></label>
          <input type="text" class="input" v-model="nummer" id="nummer">
        </div>
        <div class="cell is-col-span-4">
          <label for="stichwort" class="label">Stichwort</label>
          <input type="text" class="input" v-model="stichwort" id="stichwort">
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in stichwortOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_stichwort(opt)"
              >{{ opt }}</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-start-1">
          <label for="datum" class="label">Datum</label>
          <input type="date" v-model="datum" class="input" id="datum">
          <div class="help">
            <div class="tags">
              <span class="tag is-clickable" @click="set_heute">Heute</span>
              <span class="tag is-clickable" @click="set_gestern">Gestern</span>
            </div>
          </div>
        </div>
        <div class="cell">
          <label for="uhrzeit" class="label">Uhrzeit</label>
          <input type="time" v-model="uhrzeit" class="input" id="uhrzeit">
        </div>
        <div class="cell is-col-span-3">
          <label for="dauer" class="label">Einsatzdauer</label>
          <input type="text" v-model="dauer" class="input" id="dauer">
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in dauerOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_dauer(opt)"
              >{{ opt }}</span>
             </div>
          </div>
        </div>
        <div class="cell is-col-span-2 is-col-start-1">
          <label for="ort" class="label">Ort</label>
          <input type="text" class="input" v-model="ort" id="ort">
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in ortOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_ort(opt)"
              >{{ opt }}</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-span-3">
          <label for="einheiten" class="label">Einheiten vor Ort <span class="tag is-primary is-clickable" @click="reset_einheiten">Reset</span></label>
          <input type="text" class="input" v-model="einheiten" id="einheiten">
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in einheitenOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_einheiten(opt)"
              >{{ opt }}</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-start-1 is-col-span-5">
          <label for="bericht" class="label">Einsatzbericht <span class="tag is-primary is-clickable" @click="reset_einsatzbericht">Reset</span></label>
          <textarea class="textarea" rows="3" v-model="bericht" name="bericht"></textarea>
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in berichtOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_bericht(opt)"
              >{{ opt }}</span>
            </div>
          </div>
        </div>

        <div class="cell is-col-start-1 is-col-span-5">
          <label for="tags" class="label">Tags <span class="tag is-primary is-clickable" @click="reset_tags">Reset</span></label>
          <input type="text" class="input" v-model="tags" id="tags">
          <div class="help">
            <div class="tags">
              <span
                v-for="opt in tagOptions"
                :key="opt"
                class="tag is-clickable"
                @click="set_tags(opt)"
              >{{ opt }}</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-start-1 is-col-span-5">
          <label for="link" class="label">Link zum Beitrag</label>
          <input type="text" class="input" v-model="link" name="link"/>
        </div>
      </div>
      <div class="buttons">
        <a class="button is-outlined is-danger is-fullwidth" @click="clear_form">Formular leeren</a>
      </div>
    </div>

    <div class="column is-12">
      <hr>
      <h3 class="title is-4">Ergebnis:</h3>
      <div class="content">
        <p>Kopiere deinen Social Media Post für Facebook und Instagram:</p>
      </div>
      <div class="textarea is-fullwidth" contenteditable="true" rows="6" id="vorschau" ref="vorschauContent">
        <div v-if="nummer !== '' && jahr !== ''"><strong>&#x1F6A8; +++ Einsatzbericht {{  nummer }} / {{  jahr }} +++</strong></div>
          <div v-else-if="nummer !=='' && jahr === ''"><strong>&#x1F6A8; +++ Einsatzbericht {{ nummer }} +++</strong></div>
          <div v-else><strong>&#x1F6A8; +++ Einsatzbericht +++ </strong></div>
          <strong v-if="stichwort">&#x1F4DF; {{ stichwort }}<br/></strong>
          <strong v-if="datum">&#x23F0; {{ format_date(datum) }} {{ uhrzeit }}<br/></strong>
          <strong v-if="dauer">&#x231B; {{ dauer }}<br/></strong>
          <strong v-if="ort">&#x1F30D; {{ ort }}<br/></strong>
          <strong v-if="einheiten">&#x1F692; {{ einheiten }}<br/></strong>
          <br/>
          <div
            v-if="bericht.length > 0"
            v-for="(zeile,zeilennummer) of bericht.split('\n')"
            v-bind:key="zeilennummer" >{{ zeile }}<br/></div>
          <div v-if="link.length > 0" class="hide-on-instagram"><br/>{{ link }}<br/></div>
          <div v-if="link.length > 0" class="show-only-on-instagram" style="display:none;"><br/>&#x1F517; Link zum Bericht in unserer Bio!<br/></div>
        <div><br/>{{ tags }}</div>
      </div>

      <div class="buttons mt-4">
        <button class="button is-info" @click="copyText('all')">
          <span class="icon is-small"><i class="fas fa-copy"></i></span>
          <span>Text kopieren</span>
        </button>
        <button class="button is-warning" @click="copyText('instagram')">
          <span class="icon is-small"><i class="fab fa-instagram"></i></span>
          <span>Für Instagram kopieren</span>
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped>
.toast-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
