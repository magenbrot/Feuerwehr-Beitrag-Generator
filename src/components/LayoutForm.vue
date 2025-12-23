<script>
import moment from 'moment';

const default_tags = '#Feuerwehr #Einsatzbericht #Einsatzinfo #Firefighter #Ehrenamt #Werdau #LandkreisZwickau #Leitstelle #112 #wirfüreuch';
const default_einheiten = 'FF Werdau';

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
      ort: '',
      einheiten: default_einheiten,
      bericht: '',
      tags: default_tags,
      link: ''
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
    set_stichwort(e) {
      // console.log(e.target.innerText)

      this.stichwort = e.target.innerText;
    },
    set_heute(e) {
      // console.log(e.target.innerText)
      const now = moment();
      this.datum = now.format("YYYY-MM-DD");
      this.uhrzeit = now.format("HH:mm");
    },
    set_gestern(e) {
      // console.log(e.target.innerText)
      // console.log(new moment().format("HH:mm"))
      const yesterday = moment().subtract(1, "days");
      this.datum = yesterday.format("YYYY-MM-DD");
      this.uhrzeit = moment().format("HH:mm");
    },
    set_dauer(e) {
      // console.log(e.target.innerText)

      this.dauer = e.target.innerText;
    },
    set_ort(e) {
      // console.log(e.target.innerText)

      this.ort = e.target.innerText + ", ";
    },
    set_einheiten(e) {
      // console.log(e.target.innerText)

      if (this.einheiten.length == 0) {
        this.einheiten = e.target.innerText;
      } else {
        this.einheiten = `${this.einheiten}, ${e.target.innerText}`;
      }
    },
    set_bericht(e) {
      // console.log(e.target.innerText)

      this.bericht = e.target.innerText;
    },
    set_tags(e) {
      // console.log(e.target.innerText)

      this.tags = `${this.tags} ${e.target.innerText}`;
    },
    reset_einheiten(e) {
      // console.log(e.target.innerText)

      this.einheiten = default_einheiten;
    },
    reset_einsatzbericht(e) {
      // console.log(e.target.innerText)

      this.bericht = "";
    },
    reset_tags(e) {
      // console.log(e.target.innerText)

      this.tags = default_tags;
    },
    create_example() {
      const now = moment();
      this.nummer = "42";
      this.datum = now.startOf('month').format("YYYY-MM-DD");
      this.jahr = now.format("YYYY");
      this.uhrzeit = now.format("HH:mm");
      this.dauer = "1 Stunde";
      this.stichwort = "TMR-1 Türnotöffnung";
      this.ort = "Werdau, Bertolt-Brecht-Straße 18";
      this.einheiten = `${default_einheiten}, Rettungsdienst, Polizei`;
      this.bericht = 'Das ist ein Beispiel Einsatzbericht.';
      this.tags = default_tags;
      this.link = 'https://www.feuerwehr-werdau.de/';
    },
    clear_form() {
      this.nummer = '';
      this.datum = '';
      this.jahr = '';
      this.uhrzeit = '';
      this.dauer = '';
      this.stichwort = '';
      this.ort = '';
      this.einheiten = default_einheiten;
      this.bericht = '';
      this.tags = default_tags;
      this.link = '';
    }
  }
};
</script>

<template>
  <div class="columns is-multiline">
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
              <span class="tag is-clickable" @click="set_stichwort">ABC-1 Gasgeruch</span>
              <span class="tag is-clickable" @click="set_stichwort">BMA-/GMA-Melder</span>
              <span class="tag is-clickable" @click="set_stichwort">BR-1</span>
              <span class="tag is-clickable" @click="set_stichwort">TH-0 Ölspur</span>
              <span class="tag is-clickable" @click="set_stichwort">TMR-1 Türnotöffnung</span>
              <span class="tag is-clickable" @click="set_stichwort">TMR-2/TH-2 VU Klemm</span>
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
              <span class="tag is-clickable" @click="set_dauer">30 Minuten</span>
              <span class="tag is-clickable" @click="set_dauer">45 Minuten</span>
              <span class="tag is-clickable" @click="set_dauer">1 Stunde</span>
              <span class="tag is-clickable" @click="set_dauer">1,5 Stunden</span>
              <span class="tag is-clickable" @click="set_dauer">2 Stunden</span>
              <span class="tag is-clickable" @click="set_dauer">3 Stunden</span>
             </div>
          </div>
        </div>
        <div class="cell is-col-span-2 is-col-start-1">
          <label for="ort" class="label">Ort</label>
          <input type="text" class="input" v-model="ort" id="ort">
          <div class="help">
            <div class="tags">
              <span class="tag is-clickable" @click="set_ort">Werdau</span>
              <span class="tag is-clickable" @click="set_ort">Königswalde</span>
              <span class="tag is-clickable" @click="set_ort">Langenhessen</span>
              <span class="tag is-clickable" @click="set_ort">Leubnitz</span>
              <span class="tag is-clickable" @click="set_ort">Steinpleis</span>
              <span class="tag is-clickable" @click="set_ort">Zwickau</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-span-3">
          <label for="einheiten" class="label">Einheiten vor Ort <span class="tag is-primary is-clickable" @click="reset_einheiten">Reset</span></label>
          <input type="text" class="input" v-model="einheiten" id="einheiten">
          <div class="help">
            <div class="tags">
              <span class="tag is-clickable" @click="set_einheiten">FF Königswalde</span>
              <span class="tag is-clickable" @click="set_einheiten">FF Langenhessen</span>
              <span class="tag is-clickable" @click="set_einheiten">FF Leubnitz</span>
              <span class="tag is-clickable" @click="set_einheiten">FF Steinpleis</span>
              <span class="tag is-clickable" @click="set_einheiten">FF Fraureuth</span>
              <span class="tag is-clickable" @click="set_einheiten">BF Zwickau</span>
              <span class="tag is-clickable" @click="set_einheiten">Rettungsdienst</span>
              <span class="tag is-clickable" @click="set_einheiten">Polizei</span>
            </div>
          </div>
        </div>
        <div class="cell is-col-start-1 is-col-span-5">
          <label for="bericht" class="label">Einsatzbericht <span class="tag is-primary is-clickable" @click="reset_einsatzbericht">Reset</span></label>
          <textarea class="textarea" rows="3" v-model="bericht" name="bericht"></textarea>
          <div class="help">
            <div class="tags">
              <span class="tag is-clickable" @click="set_bericht">Der Patient wurde über das Tragetuch gerettet und an den Rettungsdienst übergeben.</span>
              <span class="tag is-clickable" @click="set_bericht">Ausgelaufene Betriebsstoffe wurden mit Bindemittel aufgenommen.</span>
            </div>
          </div>
        </div>

        <div class="cell is-col-start-1 is-col-span-5">
          <label for="tags" class="label">Tags <span class="tag is-primary is-clickable" @click="reset_tags">Reset</span></label>
          <input type="text" class="input" v-model="tags" id="tags">
          <div class="help">
            <div class="tags">
              <span class="tag is-clickable" @click="set_tags">#Brand #Feuer #Brandeinsatz #Wärmebildkamera</span>
              <span class="tag is-clickable" @click="set_tags">#BMA #GMA #Brandmeldeanlage</span>
              <span class="tag is-clickable" @click="set_tags">#TMR #Menschenrettung #Rettung</span>
              <span class="tag is-clickable" @click="set_tags">#TH #THL #TechnischeHilfeleistung</span>
              <span class="tag is-clickable" @click="set_tags">#Verkehr #Verkehrsunfall</span>
              <span class="tag is-clickable" @click="set_tags">#Türnotöffnung</span>
              <span class="tag is-clickable" @click="set_tags">#Fehlalarm</span>
              <span class="tag is-clickable" @click="set_tags">#AGT #Atemschutz #Atemschutzgeräteträger #Angriffstrupp</span>
              <span class="tag is-clickable" @click="set_tags">#HLF #Hilfeleistungslöschgruppenfahrzeug</span>
              <span class="tag is-clickable" @click="set_tags">#LF #Löschgruppenfahrzeug</span>
              <span class="tag is-clickable" @click="set_tags">#DLK #DLAK #Drehleiter</span>
              <span class="tag is-clickable" @click="set_tags">#ELW #Einsatzleitwagen</span>
              <span class="tag is-clickable" @click="set_tags">#Rettungsdienst #RTW #Rettungswagen</span>
              <span class="tag is-clickable" @click="set_tags">#Notarzt #NEF #Notarzteinsatzwagen</span>
              <span class="tag is-clickable" @click="set_tags">#Polizei #PolizeiSachsen</span>
              <span class="tag is-clickable" @click="set_tags">#Katastrophe #Katastrophenschutz</span>
              <span class="tag is-clickable" @click="set_tags">#MANV #MANE</span>
              <span class="tag is-clickable" @click="set_tags">#Betriebsmittel #Öl #Benzin #Diesel</span>
              <span class="tag is-clickable" @click="set_tags">#Baum #Kettensäge #Motorkettensäge</span>
              <span class="tag is-clickable" @click="set_tags">#Umwelt #Umweltschutz</span>
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
      <div class="textarea is-fullwidth" contenteditable="true" rows="6" id="vorschau">
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
          <div v-if="link.length > 0"><br/>{{ link }}<br/></div>
        <div><br/>{{ tags }}</div>
      </div>
    </div>

  </div>
</template>
