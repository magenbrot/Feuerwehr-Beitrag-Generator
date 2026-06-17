<script>
import { IMAGE_GENERATOR_DEFAULTS, IMAGE_FONT_OPTIONS } from '../config.js';

export default {
  name: 'ImageGenerator',
  props: {
    nummer: {
      type: [String, Number],
      default: ''
    },
    jahr: {
      type: [String, Number],
      default: ''
    },
    stichwort: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      IMAGE_GENERATOR_DEFAULTS,
      images: [],
      activeIndex: -1,
      textOverlayEnabled: true,
      customTextEnabled: false,
      customTextLine1: '',
      customTextLine2: '',
      styles: { ...IMAGE_GENERATOR_DEFAULTS },
      fontOptions: IMAGE_FONT_OPTIONS,
      logoImageElement: null,
      logoAspectRatio: 1.0,
      
      // Drag & drop state
      isDragOver: false,
      
      // Interaction state
      isDragging: false,
      startX: 0,
      startY: 0
    };
  },
  computed: {
    activeImage() {
      if (this.activeIndex >= 0 && this.activeIndex < this.images.length) {
        return this.images[this.activeIndex];
      }
      return null;
    },
    nummerText() {
      return this.nummer || '--';
    },
    jahrText() {
      return this.jahr || new Date().getFullYear();
    },
    stichwortText() {
      return this.stichwort || 'Einsatzbericht';
    }
  },
  watch: {
    // Redraw canvas on prop changes (Incident Number, Year, Keyword)
    nummerText() { this.renderActiveCanvas(); },
    jahrText() { this.renderActiveCanvas(); },
    stichwortText() { this.renderActiveCanvas(); },
    
    // Redraw canvas on style changes
    'styles.textColor'() { this.renderActiveCanvas(); },
    'styles.backgroundColor'() { this.renderActiveCanvas(); },
    'styles.backgroundOpacity'() { this.renderActiveCanvas(); },
    'styles.borderColor'() { this.renderActiveCanvas(); },
    'styles.borderWidth'() { this.renderActiveCanvas(); },
    'styles.textOutlineColor'() { this.renderActiveCanvas(); },
    'styles.textOutlineWidth'() { this.renderActiveCanvas(); },
    'styles.fontFamily'() { this.renderActiveCanvas(); },
    'styles.fontSize'() { this.renderActiveCanvas(); },
    'styles.padding'() { this.renderActiveCanvas(); },
    'styles.position'() { this.renderActiveCanvas(); },
    'styles.logoVisible'() { this.renderActiveCanvas(); },
    'styles.logoScale'() { this.renderActiveCanvas(); },
    
    textOverlayEnabled() { this.renderActiveCanvas(); },
    customTextEnabled() { this.renderActiveCanvas(); },
    customTextLine1() { this.renderActiveCanvas(); },
    customTextLine2() { this.renderActiveCanvas(); },
    
    activeIndex() {
      this.renderActiveCanvas();
    }
  },
  mounted() {
    this.loadDefaultLogo();
    
    // Redraw when fonts finish loading (since Google Fonts load asynchronously)
    if (document.fonts) {
      document.fonts.ready.then(() => {
        this.renderActiveCanvas();
      });
    }
  },
  beforeUnmount() {
    // Revoke all object URLs to prevent memory leaks
    this.images.forEach(img => {
      if (img.url) URL.revokeObjectURL(img.url);
    });
  },
  methods: {
    loadDefaultLogo() {
      const img = new Image();
      img.onload = () => {
        this.logoImageElement = img;
        this.logoAspectRatio = img.width / img.height;
        this.renderActiveCanvas();
      };
      img.onerror = () => {
        console.error('Failed to load default logo: ' + this.styles.logoPath);
      };
      img.src = this.styles.logoPath;
    },
    
    handleLogoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          this.logoImageElement = img;
          this.logoAspectRatio = img.width / img.height;
          this.renderActiveCanvas();
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    resetLogo() {
      this.styles.logoPath = IMAGE_GENERATOR_DEFAULTS.logoPath;
      this.loadDefaultLogo();
    },
    
    resetStyles() {
      this.styles = { ...IMAGE_GENERATOR_DEFAULTS };
      this.loadDefaultLogo();
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    onDragOver(e) {
      e.preventDefault();
      this.isDragOver = true;
    },

    onDragLeave() {
      this.isDragOver = false;
    },

    onDrop(e) {
      e.preventDefault();
      this.isDragOver = false;
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.processFiles(files);
      }
    },

    onFileChange(e) {
      const files = e.target.files;
      if (files.length > 0) {
        this.processFiles(files);
      }
    },

    processFiles(files) {
      const currentCount = this.images.length;
      const availableSlots = 10 - currentCount;
      
      if (availableSlots <= 0) {
        alert('Maximal 10 Bilder erlaubt.');
        return;
      }

      const filesToProcess = Array.from(files).slice(0, availableSlots);
      if (files.length > availableSlots) {
        alert(`Es können nur noch ${availableSlots} Bilder hinzugefügt werden (Limit von 10 Bildern erreicht).`);
      }

      filesToProcess.forEach(file => {
        if (!file.type.startsWith('image/')) {
          alert(`Datei "${file.name}" ist kein Bild.`);
          return;
        }

        const objectUrl = URL.createObjectURL(file);
        const imgItem = {
          id: Date.now() + Math.random().toString(36).substr(2, 9),
          file: file,
          name: file.name,
          url: objectUrl,
          zoom: 1.0,
          cropX: 0,
          cropY: 0,
          cropSize: 0,
          imageElement: null,
          imgLoaded: false
        };

        const img = new Image();
        img.onload = () => {
          imgItem.imageElement = img;
          imgItem.imgLoaded = true;
          
          // Initialize crop rectangle centered to cover the smaller dimension
          const maxSize = Math.min(img.width, img.height);
          imgItem.cropSize = maxSize;
          imgItem.cropX = (img.width - maxSize) / 2;
          imgItem.cropY = (img.height - maxSize) / 2;
          
          // Re-render canvas if this became the active image
          if (this.activeIndex === this.images.indexOf(imgItem)) {
            this.renderActiveCanvas();
          }
        };
        img.src = objectUrl;

        this.images.push(imgItem);
      });

      if (this.activeIndex === -1 && this.images.length > 0) {
        this.activeIndex = 0;
      }
    },

    removeImage(index) {
      const removed = this.images.splice(index, 1)[0];
      if (removed && removed.url) {
        URL.revokeObjectURL(removed.url);
      }
      
      if (this.images.length === 0) {
        this.activeIndex = -1;
        this.clearCanvas();
      } else if (this.activeIndex >= this.images.length) {
        this.activeIndex = this.images.length - 1;
      } else {
        this.renderActiveCanvas();
      }
    },

    clearCanvas() {
      const canvas = this.$refs.editorCanvas;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, 1080, 1080);
      ctx.fillStyle = '#f5f5f5';
      ctx.fillRect(0, 0, 1080, 1080);
      ctx.fillStyle = '#7a7a7a';
      ctx.font = '36px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Kein Bild ausgewählt', 540, 540);
    },

    renderActiveCanvas() {
      const canvas = this.$refs.editorCanvas;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      this.drawPreviewCanvas(ctx, this.activeImage);
    },

    onZoomChange() {
      const imgObj = this.activeImage;
      if (!imgObj || !imgObj.imgLoaded) return;
      
      const img = imgObj.imageElement;
      const maxSize = Math.min(img.width, img.height);
      const newCropSize = maxSize / imgObj.zoom;
      
      const centerX = imgObj.cropX + imgObj.cropSize / 2;
      const centerY = imgObj.cropY + imgObj.cropSize / 2;
      
      imgObj.cropSize = newCropSize;
      imgObj.cropX = Math.max(0, Math.min(img.width - newCropSize, centerX - newCropSize / 2));
      imgObj.cropY = Math.max(0, Math.min(img.height - newCropSize, centerY - newCropSize / 2));
      
      this.renderActiveCanvas();
    },

    drawPreviewCanvas(ctx, imgObj) {
      if (!imgObj || !imgObj.imgLoaded) {
        this.clearCanvas();
        return;
      }
      const img = imgObj.imageElement;
      const W = img.width;
      const H = img.height;
      
      const canvas = this.$refs.editorCanvas;
      if (canvas.width !== W || canvas.height !== H) {
        canvas.width = W;
        canvas.height = H;
      }
      
      ctx.clearRect(0, 0, W, H);
      
      // 1. Draw original full image
      ctx.drawImage(img, 0, 0);
      
      // 2. Draw dark overlay outside crop square
      ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
      const cx = imgObj.cropX;
      const cy = imgObj.cropY;
      const cs = imgObj.cropSize;
      
      ctx.fillRect(0, 0, W, cy);
      ctx.fillRect(0, cy + cs, W, H - (cy + cs));
      ctx.fillRect(0, cy, cx, cs);
      ctx.fillRect(cx + cs, cy, W - (cx + cs), cs);
      
      // 3. Draw dashed border around crop square
      ctx.strokeStyle = '#ffffff';
      const lineWidth = Math.max(3, W * 0.002);
      ctx.lineWidth = lineWidth;
      ctx.setLineDash([lineWidth * 3, lineWidth * 3]);
      ctx.strokeRect(cx, cy, cs, cs);
      ctx.setLineDash([]);
      
      // 4. Draw overlays relative to crop square scaled down
      const scale = cs / 1080;
      const fontFamily = this.styles.fontFamily;
      const fontSize = (parseInt(this.styles.fontSize) || 48) * scale;
      
      const drawTextWithOutline = (text, tx, ty, size, align = 'left') => {
        ctx.save();
        ctx.font = `bold ${size}px ${fontFamily}`;
        ctx.textAlign = align;
        if (this.styles.textOutlineWidth > 0 && this.styles.textOutlineColor) {
          ctx.lineWidth = (parseInt(this.styles.textOutlineWidth) || 0) * scale;
          ctx.strokeStyle = this.styles.textOutlineColor;
          ctx.lineJoin = 'round';
          ctx.strokeText(text, tx, ty);
        }
        ctx.fillStyle = this.styles.textColor;
        ctx.fillText(text, tx, ty);
        ctx.restore();
      };

      // Draw text overlay if it's the first image
      if (this.textOverlayEnabled && this.activeIndex === 0) {
        ctx.save();
        
        if (this.styles.position === 'center-werdau') {
          ctx.textBaseline = 'middle';
          const yStart = cy + 220 * scale;
          const arrowLine = "«" + "─".repeat(14) + "»";
          
          drawTextWithOutline(arrowLine, cx + 540 * scale, yStart, fontSize * 0.75, 'center');
          drawTextWithOutline("EINSATZ !", cx + 540 * scale, yStart + fontSize * 1.0, fontSize * 1.1, 'center');
          const numberYearStr = this.customTextEnabled ? this.customTextLine1 : `${this.nummerText} / ${this.jahrText}`;
          drawTextWithOutline(numberYearStr.toUpperCase(), cx + 540 * scale, yStart + fontSize * 2.3, fontSize * 1.45, 'center');
          const stichwortStr = this.customTextEnabled ? this.customTextLine2 : this.stichwortText;
          drawTextWithOutline(stichwortStr.toUpperCase(), cx + 540 * scale, yStart + fontSize * 3.4, fontSize * 0.55, 'center');
          drawTextWithOutline(arrowLine, cx + 540 * scale, yStart + fontSize * 4.1, fontSize * 0.75, 'center');
        } else {
          let line1 = this.customTextEnabled ? this.customTextLine1 : `Einsatz ${this.nummerText} / ${this.jahrText}`;
          let line2 = this.customTextEnabled ? this.customTextLine2 : this.stichwortText;
          const padding = (parseInt(this.styles.padding) || 24) * scale;
          const borderWidth = (parseInt(this.styles.borderWidth) || 0) * scale;
          
          ctx.font = `bold ${fontSize}px ${fontFamily}`;
          ctx.textBaseline = 'top';
          
          const width1 = ctx.measureText(line1).width;
          const width2 = ctx.measureText(line2).width;
          const maxTextWidth = Math.max(width1, width2);
          
          const lineSpacing = 12 * scale;
          const boxWidth = maxTextWidth + padding * 2;
          const boxHeight = fontSize * 2 + lineSpacing + padding * 2;
          
          const margin = 40 * scale;
          let bx = cx + margin;
          let by = cy + margin;
          let isBanner = false;
          
          if (this.styles.position === 'top-left') {
            bx = cx + margin;
            by = cy + margin;
          } else if (this.styles.position === 'top-right') {
            bx = cx + cs - boxWidth - margin;
            by = cy + margin;
          } else if (this.styles.position === 'bottom-left') {
            bx = cx + margin;
            by = cy + cs - boxHeight - margin;
          } else if (this.styles.position === 'top-banner') {
            bx = cx;
            by = cy;
            isBanner = true;
          } else if (this.styles.position === 'bottom-banner') {
            bx = cx;
            by = cy + cs - boxHeight;
            isBanner = true;
          }
          
          ctx.fillStyle = this.hexToRgba(this.styles.backgroundColor, this.styles.backgroundOpacity);
          if (isBanner) {
            ctx.fillRect(bx, by, cs, boxHeight);
          } else {
            this.drawRoundedRect(ctx, bx, by, boxWidth, boxHeight, 8 * scale);
            ctx.fill();
          }
          
          if (borderWidth > 0 && this.styles.borderColor) {
            ctx.strokeStyle = this.styles.borderColor;
            ctx.lineWidth = borderWidth;
            if (isBanner) {
              ctx.beginPath();
              if (this.styles.position === 'top-banner') {
                ctx.moveTo(cx, by + boxHeight - borderWidth/2);
                ctx.lineTo(cx + cs, by + boxHeight - borderWidth/2);
              } else {
                ctx.moveTo(cx, by + borderWidth/2);
                ctx.lineTo(cx + cs, by + borderWidth/2);
              }
              ctx.stroke();
            } else {
              ctx.stroke();
            }
          }
          
          const tx = isBanner ? cx + cs / 2 : bx + padding;
          const ty1 = by + padding;
          const ty2 = by + padding + fontSize + lineSpacing;
          
          drawTextWithOutline(line1, tx, ty1, fontSize, isBanner ? 'center' : 'left');
          drawTextWithOutline(line2, tx, ty2, fontSize, isBanner ? 'center' : 'left');
        }
        ctx.restore();
      }
      
      // Draw Logo on all images
      if (this.styles.logoVisible && this.logoImageElement) {
        ctx.save();
        const logoScale = this.styles.logoScale || 1.0;
        const logoW = 180 * logoScale * scale;
        const logoH = (180 / this.logoAspectRatio) * logoScale * scale;
        const margin = 40 * scale;
        const lx = cx + cs - logoW - margin;
        const ly = cy + cs - logoH - margin;
        
        ctx.drawImage(this.logoImageElement, lx, ly, logoW, logoH);
        ctx.restore();
      }
    },

    drawCroppedCanvas(ctx, imgObj, isFirstImage) {
      if (!imgObj || !imgObj.imgLoaded) return;
      const img = imgObj.imageElement;
      
      // 1. Draw Cropped image scaled to 1080x1080
      ctx.drawImage(img, imgObj.cropX, imgObj.cropY, imgObj.cropSize, imgObj.cropSize, 0, 0, 1080, 1080);
      
      const fontFamily = this.styles.fontFamily;
      const fontSize = parseInt(this.styles.fontSize) || 48;

      // Helper for outlined text
      const drawTextWithOutline = (text, tx, ty, size, align = 'left') => {
        ctx.save();
        ctx.font = `bold ${size}px ${fontFamily}`;
        ctx.textAlign = align;
        if (this.styles.textOutlineWidth > 0 && this.styles.textOutlineColor) {
          ctx.lineWidth = parseInt(this.styles.textOutlineWidth) || 0;
          ctx.strokeStyle = this.styles.textOutlineColor;
          ctx.lineJoin = 'round';
          ctx.strokeText(text, tx, ty);
        }
        ctx.fillStyle = this.styles.textColor;
        ctx.fillText(text, tx, ty);
        ctx.restore();
      };

      // 2. Draw Text Overlay
      if (this.textOverlayEnabled && isFirstImage) {
        let line1 = this.customTextEnabled ? this.customTextLine1 : `Einsatz ${this.nummerText} / ${this.jahrText}`;
        let line2 = this.customTextEnabled ? this.customTextLine2 : this.stichwortText;

        ctx.save();
        const padding = parseInt(this.styles.padding) || 24;
        const borderWidth = parseInt(this.styles.borderWidth) || 0;
        
        ctx.font = `bold ${fontSize}px ${fontFamily}`;

        if (this.styles.position === 'center-werdau') {
          ctx.textBaseline = 'middle';
          const yStart = 220;
          const arrowLine = "«" + "─".repeat(14) + "»";
          
          drawTextWithOutline(arrowLine, 540, yStart, fontSize * 0.75, 'center');
          drawTextWithOutline("EINSATZ !", 540, yStart + fontSize * 1.0, fontSize * 1.1, 'center');
          const numberYearStr = this.customTextEnabled ? this.customTextLine1 : `${this.nummerText} / ${this.jahrText}`;
          drawTextWithOutline(numberYearStr.toUpperCase(), 540, yStart + fontSize * 2.3, fontSize * 1.45, 'center');
          const stichwortStr = this.customTextEnabled ? this.customTextLine2 : this.stichwortText;
          drawTextWithOutline(stichwortStr.toUpperCase(), 540, yStart + fontSize * 3.4, fontSize * 0.55, 'center');
          drawTextWithOutline(arrowLine, 540, yStart + fontSize * 4.1, fontSize * 0.75, 'center');
        } else {
          ctx.textBaseline = 'top';
          const width1 = ctx.measureText(line1).width;
          const width2 = ctx.measureText(line2).width;
          const maxTextWidth = Math.max(width1, width2);
          
          const lineSpacing = 12;
          const boxWidth = maxTextWidth + padding * 2;
          const boxHeight = fontSize * 2 + lineSpacing + padding * 2;
          
          const margin = 40;
          let bx = margin;
          let by = margin;
          let isBanner = false;
          
          if (this.styles.position === 'top-left') {
            bx = margin;
            by = margin;
          } else if (this.styles.position === 'top-right') {
            bx = 1080 - boxWidth - margin;
            by = margin;
          } else if (this.styles.position === 'bottom-left') {
            bx = margin;
            by = 1080 - boxHeight - margin;
          } else if (this.styles.position === 'top-banner') {
            bx = 0;
            by = 0;
            isBanner = true;
          } else if (this.styles.position === 'bottom-banner') {
            bx = 0;
            by = 1080 - boxHeight;
            isBanner = true;
          }
          
          ctx.fillStyle = this.hexToRgba(this.styles.backgroundColor, this.styles.backgroundOpacity);
          if (isBanner) {
            ctx.fillRect(bx, by, 1080, boxHeight);
          } else {
            this.drawRoundedRect(ctx, bx, by, boxWidth, boxHeight, 8);
            ctx.fill();
          }
          
          if (borderWidth > 0 && this.styles.borderColor) {
            ctx.strokeStyle = this.styles.borderColor;
            ctx.lineWidth = borderWidth;
            if (isBanner) {
              ctx.beginPath();
              if (this.styles.position === 'top-banner') {
                ctx.moveTo(0, boxHeight - borderWidth/2);
                ctx.lineTo(1080, boxHeight - borderWidth/2);
              } else {
                ctx.moveTo(0, by + borderWidth/2);
                ctx.lineTo(1080, by + borderWidth/2);
              }
              ctx.stroke();
            } else {
              ctx.stroke();
            }
          }
          
          const tx = isBanner ? 540 : bx + padding;
          const ty1 = by + padding;
          const ty2 = by + padding + fontSize + lineSpacing;
          
          drawTextWithOutline(line1, tx, ty1, fontSize, isBanner ? 'center' : 'left');
          drawTextWithOutline(line2, tx, ty2, fontSize, isBanner ? 'center' : 'left');
        }
        
        ctx.restore();
      }

      // 3. Draw Logo Overlay
      if (this.styles.logoVisible && this.logoImageElement) {
        ctx.save();
        const scale = this.styles.logoScale || 1.0;
        const logoW = 180 * scale;
        const logoH = (180 / this.logoAspectRatio) * scale;
        
        const margin = 40;
        const lx = 1080 - logoW - margin;
        const ly = 1080 - logoH - margin;
        
        ctx.drawImage(this.logoImageElement, lx, ly, logoW, logoH);
        ctx.restore();
      }
    },

    // Drag/Touch Handlers on Preview
    onMouseDown(e) {
      if (!this.activeImage) return;
      const canvas = this.$refs.editorCanvas;
      const rect = canvas.getBoundingClientRect();
      const dispX = e.clientX - rect.left;
      const dispY = e.clientY - rect.top;
      
      const mouseX = dispX * (canvas.width / rect.width);
      const mouseY = dispY * (canvas.height / rect.height);
      
      const imgObj = this.activeImage;
      const cx = imgObj.cropX;
      const cy = imgObj.cropY;
      const cs = imgObj.cropSize;
      
      const isInside = (mouseX >= cx && mouseX <= cx + cs && mouseY >= cy && mouseY <= cy + cs);
      
      if (!isInside) {
        imgObj.cropX = Math.max(0, Math.min(canvas.width - cs, mouseX - cs / 2));
        imgObj.cropY = Math.max(0, Math.min(canvas.height - cs, mouseY - cs / 2));
        this.renderActiveCanvas();
      }
      
      this.isDragging = true;
      this.startX = e.clientX;
      this.startY = e.clientY;
    },
    
    onMouseMove(e) {
      if (!this.isDragging || !this.activeImage) return;
      const dx = e.clientX - this.startX;
      const dy = e.clientY - this.startY;
      
      const canvas = this.$refs.editorCanvas;
      const rect = canvas.getBoundingClientRect();
      const scaleFactorX = canvas.width / rect.width;
      const scaleFactorY = canvas.height / rect.height;
      
      const imgObj = this.activeImage;
      imgObj.cropX += dx * scaleFactorX;
      imgObj.cropY += dy * scaleFactorY;
      
      imgObj.cropX = Math.max(0, Math.min(canvas.width - imgObj.cropSize, imgObj.cropX));
      imgObj.cropY = Math.max(0, Math.min(canvas.height - imgObj.cropSize, imgObj.cropY));
      
      this.startX = e.clientX;
      this.startY = e.clientY;
      
      this.renderActiveCanvas();
    },
    
    onMouseUpOrLeave() {
      this.isDragging = false;
    },
    
    onTouchStart(e) {
      if (!this.activeImage || e.touches.length !== 1) return;
      const touch = e.touches[0];
      
      const canvas = this.$refs.editorCanvas;
      const rect = canvas.getBoundingClientRect();
      const dispX = touch.clientX - rect.left;
      const dispY = touch.clientY - rect.top;
      
      const mouseX = dispX * (canvas.width / rect.width);
      const mouseY = dispY * (canvas.height / rect.height);
      
      const imgObj = this.activeImage;
      const cx = imgObj.cropX;
      const cy = imgObj.cropY;
      const cs = imgObj.cropSize;
      
      const isInside = (mouseX >= cx && mouseX <= cx + cs && mouseY >= cy && mouseY <= cy + cs);
      
      if (!isInside) {
        imgObj.cropX = Math.max(0, Math.min(canvas.width - cs, mouseX - cs / 2));
        imgObj.cropY = Math.max(0, Math.min(canvas.height - cs, mouseY - cs / 2));
        this.renderActiveCanvas();
      }
      
      this.isDragging = true;
      this.startX = touch.clientX;
      this.startY = touch.clientY;
    },
    
    onTouchMove(e) {
      if (!this.isDragging || !this.activeImage || e.touches.length !== 1) return;
      const touch = e.touches[0];
      const dx = touch.clientX - this.startX;
      const dy = touch.clientY - this.startY;
      
      const canvas = this.$refs.editorCanvas;
      const rect = canvas.getBoundingClientRect();
      const scaleFactorX = canvas.width / rect.width;
      const scaleFactorY = canvas.height / rect.height;
      
      const imgObj = this.activeImage;
      imgObj.cropX += dx * scaleFactorX;
      imgObj.cropY += dy * scaleFactorY;
      
      imgObj.cropX = Math.max(0, Math.min(canvas.width - imgObj.cropSize, imgObj.cropX));
      imgObj.cropY = Math.max(0, Math.min(canvas.height - imgObj.cropSize, imgObj.cropY));
      
      this.startX = touch.clientX;
      this.startY = touch.clientY;
      
      this.renderActiveCanvas();
    },
    
    onTouchEnd() {
      this.isDragging = false;
    },
    
    onWheel(e) {
      if (!this.activeImage) return;
      e.preventDefault();
      
      const zoomDelta = e.deltaY * -0.001;
      this.activeImage.zoom = Math.min(5.0, Math.max(1.0, this.activeImage.zoom + zoomDelta));
      this.onZoomChange();
    },

    // Rendering Helpers
    drawRoundedRect(ctx, x, y, width, height, radius) {
      ctx.beginPath();
      ctx.moveTo(x + radius, y);
      ctx.lineTo(x + width - radius, y);
      ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
      ctx.lineTo(x + width, y + height - radius);
      ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
      ctx.lineTo(x + radius, y + height);
      ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
      ctx.lineTo(x, y + radius);
      ctx.quadraticCurveTo(x, y, x + radius, y);
      ctx.closePath();
    },

    hexToRgba(hex, alpha) {
      let c;
      if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c = hex.substring(1).split('');
        if(c.length === 3){
          c = [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x' + c.join('');
        return 'rgba(' + [(c>>16)&255, (c>>8)&255, c&255].join(',') + ',' + alpha + ')';
      }
      return hex;
    },

    // Download handlers
    downloadActive() {
      if (!this.activeImage) return;
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 1080;
      tempCanvas.height = 1080;
      const tempCtx = tempCanvas.getContext('2d');
      
      this.drawCroppedCanvas(tempCtx, this.activeImage, this.activeIndex === 0);
      
      const dataUrl = tempCanvas.toDataURL('image/jpeg', 0.95);
      const link = document.createElement('a');
      link.download = `Einsatz_${this.nummerText || 'Bericht'}_${this.jahrText}_${this.activeIndex + 1}.jpg`;
      link.href = dataUrl;
      link.click();
    },

    downloadAll() {
      if (this.images.length === 0) return;
      
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 1080;
      tempCanvas.height = 1080;
      const tempCtx = tempCanvas.getContext('2d');
      
      this.images.forEach((imgObj, idx) => {
        if (!imgObj.imgLoaded) return;
        
        tempCtx.clearRect(0, 0, 1080, 1080);
        this.drawCroppedCanvas(tempCtx, imgObj, idx === 0);
        
        const dataUrl = tempCanvas.toDataURL('image/jpeg', 0.95);
        const link = document.createElement('a');
        link.download = `Einsatz_${this.nummerText || 'Bericht'}_${this.jahrText}_${idx + 1}.jpg`;
        link.href = dataUrl;
        link.click();
      });
    }
  }
};
</script>

<template>
  <div class="image-generator">
    <!-- Dropzone / Image Uploader -->
    <div
      class="upload-box mb-4"
      :class="{ 'is-dragover': isDragOver }"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
      @click="triggerFileInput"
    >
      <input
        type="file"
        ref="fileInput"
        multiple
        accept="image/*"
        class="is-hidden"
        @change="onFileChange"
      />
      <div class="has-text-centered py-4">
        <span class="icon is-large has-text-grey-light">
          <i class="fas fa-cloud-upload-alt fa-2x"></i>
        </span>
        <p class="has-text-weight-semibold">Bilder per Drag & Drop hierher ziehen oder klicken</p>
        <p class="is-size-7 has-text-grey">Maximal 10 Bilder insgesamt ({{ images.length }}/10)</p>
      </div>
    </div>

    <!-- Thumbnails list -->
    <div v-if="images.length > 0" class="thumbnails-list mb-4">
      <div
        v-for="(img, idx) in images"
        :key="img.id"
        class="thumb-item"
        :class="{ 'is-active': idx === activeIndex }"
        @click="activeIndex = idx"
      >
        <img :src="img.url" alt="Miniaturansicht" />
        <button class="delete-btn" @click.stop="removeImage(idx)">
          <i class="fas fa-times-circle"></i>
        </button>
      </div>
    </div>

    <!-- Editor Workspace -->
    <div v-if="images.length > 0" class="columns is-multiline">
      <!-- Left: Interactive Canvas Crop Preview -->
      <div class="column is-12-tablet is-6-desktop">
        <div class="canvas-container-outer">
          <canvas
            ref="editorCanvas"
            width="1080"
            height="1080"
            @mousedown="onMouseDown"
            @mousemove="onMouseMove"
            @mouseup="onMouseUpOrLeave"
            @mouseleave="onMouseUpOrLeave"
            @touchstart="onTouchStart"
            @touchmove="onTouchMove"
            @touchend="onTouchEnd"
            @wheel="onWheel"
          ></canvas>
        </div>
        
        <!-- Zoom Slider -->
        <div class="field mt-3">
          <label class="label is-small flex-label-row">
            <span>Zoom: {{ Math.round(activeImage.zoom * 100) }}%</span>
            <span class="has-text-grey is-size-7">(Scrollen im Bild geht auch)</span>
          </label>
          <div class="control">
            <input
              type="range"
              class="slider-input"
              v-model.number="activeImage.zoom"
              min="1.0"
              max="3.0"
              step="0.05"
              @input="renderActiveCanvas"
            />
          </div>
        </div>
        
        <p class="help has-text-centered has-text-grey mb-4">
          <i class="fas fa-arrows-alt"></i> Klicke und ziehe das Bild im Vorschaubereich, um den Ausschnitt zu verschieben.
        </p>

        <!-- Actions -->
        <div class="buttons">
          <button class="button is-success is-fullwidth" @click="downloadActive">
            <span class="icon"><i class="fas fa-download"></i></span>
            <span>Aktuelles Bild herunterladen</span>
          </button>
          <button
            v-if="images.length > 1"
            class="button is-link is-outlined is-fullwidth mt-2"
            @click="downloadAll"
          >
            <span class="icon"><i class="fas fa-images"></i></span>
            <span>Alle {{ images.length }} Bilder herunterladen</span>
          </button>
        </div>
      </div>

      <!-- Right: Overlay Customization Settings -->
      <div class="column is-12-tablet is-6-desktop">
        <div class="card editor-controls-card">
          <div class="card-content py-3">
            <h4 class="title is-5 mb-3">Text-Overlay</h4>
            
            <!-- Toggle Overlay -->
            <div class="field mb-3">
              <label class="checkbox has-text-weight-bold">
                <input type="checkbox" v-model="textOverlayEnabled" />
                Text-Overlay anzeigen
              </label>
            </div>

            <div v-if="textOverlayEnabled">
              <!-- Custom Text toggle -->
              <div class="field mb-3">
                <label class="checkbox is-size-7">
                  <input type="checkbox" v-model="customTextEnabled" />
                  Text manuell überschreiben (statt Einsatzdaten)
                </label>
              </div>

              <!-- Custom Text Inputs -->
              <div v-if="customTextEnabled" class="box p-3 mb-3">
                <div class="field mb-2">
                  <label class="label is-small">Zeile 1</label>
                  <div class="control">
                    <input type="text" class="input is-small" v-model="customTextLine1" placeholder="z.B. Einsatz 54 / 2026" />
                  </div>
                </div>
                <div class="field">
                  <label class="label is-small">Zeile 2</label>
                  <div class="control">
                    <input type="text" class="input is-small" v-model="customTextLine2" placeholder="z.B. TH-0 Ölspur" />
                  </div>
                </div>
              </div>

              <div class="columns is-mobile is-multiline is-gapless-mobile">
                <!-- Text Color -->
                <div class="column is-6 pr-2 mb-2">
                  <label class="label is-small mb-1">Textfarbe</label>
                  <div class="color-picker-wrapper">
                    <input type="color" v-model="styles.textColor" />
                    <span class="is-size-7 ml-1">{{ styles.textColor }}</span>
                  </div>
                </div>
                <!-- Background Color -->
                <div class="column is-6 pl-2 mb-2">
                  <label class="label is-small mb-1">Hintergrund</label>
                  <div class="color-picker-wrapper">
                    <input type="color" v-model="styles.backgroundColor" />
                    <span class="is-size-7 ml-1">{{ styles.backgroundColor }}</span>
                  </div>
                </div>
                <!-- Background Opacity -->
                <div class="column is-12 mb-3">
                  <label class="label is-small mb-1">Hintergrund-Deckkraft: {{ Math.round(styles.backgroundOpacity * 100) }}%</label>
                  <input type="range" class="slider-input" min="0" max="1" step="0.05" v-model.number="styles.backgroundOpacity" />
                </div>
                <!-- Border Color -->
                <div class="column is-6 pr-2 mb-2">
                  <label class="label is-small mb-1">Rahmenfarbe</label>
                  <div class="color-picker-wrapper">
                    <input type="color" v-model="styles.borderColor" />
                    <span class="is-size-7 ml-1">{{ styles.borderColor }}</span>
                  </div>
                </div>
                <!-- Border Width -->
                <div class="column is-6 pl-2 mb-2">
                  <label class="label is-small mb-1">Rahmenstärke: {{ styles.borderWidth }}px</label>
                  <input type="range" class="slider-input" min="0" max="15" step="1" v-model.number="styles.borderWidth" />
                </div>
                <!-- Text Outline Color -->
                <div class="column is-6 pr-2 mb-2">
                  <label class="label is-small mb-1">Umrandungsfarbe</label>
                  <div class="color-picker-wrapper">
                    <input type="color" v-model="styles.textOutlineColor" />
                    <span class="is-size-7 ml-1">{{ styles.textOutlineColor }}</span>
                  </div>
                </div>
                <!-- Text Outline Width -->
                <div class="column is-6 pl-2 mb-2">
                  <label class="label is-small mb-1">Umrandungsstärke: {{ styles.textOutlineWidth }}px</label>
                  <input type="range" class="slider-input" min="0" max="15" step="1" v-model.number="styles.textOutlineWidth" />
                </div>
                <!-- Font Family -->
                <div class="column is-12 mb-3">
                  <label class="label is-small mb-1">Schriftart</label>
                  <div class="select is-small is-fullwidth">
                    <select v-model="styles.fontFamily">
                      <option v-for="f in fontOptions" :key="f.value" :value="f.value">{{ f.label }}</option>
                    </select>
                  </div>
                </div>
                <!-- Font Size -->
                <div class="column is-6 pr-2 mb-3">
                  <label class="label is-small mb-1">Schriftgröße: {{ styles.fontSize }}px</label>
                  <input type="range" class="slider-input" min="24" max="64" step="1" v-model.number="styles.fontSize" />
                </div>
                <!-- Padding -->
                <div class="column is-6 pl-2 mb-3">
                  <label class="label is-small mb-1">Abstand innen: {{ styles.padding }}px</label>
                  <input type="range" class="slider-input" min="10" max="60" step="1" v-model.number="styles.padding" />
                </div>
                <!-- Position -->
                <div class="column is-12 mb-3">
                  <label class="label is-small mb-1">Position des Text-Overlays</label>
                  <div class="select is-small is-fullwidth">
                    <select v-model="styles.position">
                      <option value="center-werdau">Werdau Design (Zentriert mit Pfeilen)</option>
                      <option value="top-left">Ecke oben links (Floating)</option>
                      <option value="top-right">Ecke oben rechts (Floating)</option>
                      <option value="bottom-left">Ecke unten links (Floating)</option>
                      <option value="top-banner">Volle Breite oben (Banner)</option>
                      <option value="bottom-banner">Volle Breite unten (Banner)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <hr class="my-3">
            
            <h4 class="title is-5 mb-3">Logo-Overlay</h4>
            <!-- Logo Visibility -->
            <div class="field mb-3">
              <label class="checkbox">
                <input type="checkbox" v-model="styles.logoVisible" />
                Logo in rechter unterer Ecke anzeigen
              </label>
            </div>
            
            <div v-if="styles.logoVisible">
              <div class="field mb-3">
                <label class="label is-small mb-1">Logo-Größe: {{ Math.round(styles.logoScale * 100) }}%</label>
                <input type="range" class="slider-input" min="0.4" max="2.0" step="0.05" v-model.number="styles.logoScale" />
              </div>
              
              <div class="field">
                <label class="label is-small mb-1">Eigenes Logo hochladen</label>
                <div class="file is-small is-info">
                  <label class="file-label">
                    <input class="file-input" type="file" accept="image/*" @change="handleLogoUpload">
                    <span class="file-cta">
                      <span class="file-icon"><i class="fas fa-upload"></i></span>
                      <span class="file-label">Logo auswählen…</span>
                    </span>
                  </label>
                  <button v-if="styles.logoPath !== IMAGE_GENERATOR_DEFAULTS.logoPath" class="button is-small is-light ml-2" @click="resetLogo">
                    Reset
                  </button>
                </div>
              </div>
            </div>
            
            <hr class="my-3">
            
            <!-- Reset Button -->
            <button class="button is-small is-danger is-outlined is-fullwidth" @click="resetStyles">
              <span class="icon"><i class="fas fa-undo"></i></span>
              <span>Design auf Standard zurücksetzen</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.upload-box {
  border: 3px dashed #dbdbdb;
  border-radius: 8px;
  background-color: #fafafa;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.upload-box:hover, .upload-box.is-dragover {
  border-color: #e63946;
  background-color: #fff5f5;
}

.thumbnails-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  max-height: 180px;
  overflow-y: auto;
  padding: 8px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
  background: #fcfcfc;
}

.thumb-item {
  position: relative;
  width: 70px;
  height: 70px;
  border-radius: 6px;
  border: 2px solid #dbdbdb;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
}

.thumb-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-item.is-active {
  border-color: #e63946;
  box-shadow: 0 0 8px rgba(230, 57, 70, 0.4);
}

.thumb-item:hover {
  transform: scale(1.05);
}

.delete-btn {
  position: absolute;
  top: 1px;
  right: 1px;
  background: white;
  border: none;
  border-radius: 50%;
  padding: 0;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e63946;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

.canvas-container-outer {
  width: 100%;
  max-width: 480px;
  border: 2px solid #dbdbdb;
  border-radius: 8px;
  background-color: #f0f0f0;
  overflow: hidden;
  margin: 0 auto;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.canvas-container-outer canvas {
  width: 100%;
  max-height: 480px;
  display: block;
  cursor: move;
  object-fit: contain;
}

.slider-input {
  width: 100%;
  margin: 8px 0;
  accent-color: #e63946;
}

.color-picker-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid #dbdbdb;
  border-radius: 4px;
  padding: 4px 8px;
  background: white;
  height: 30px;
}

.color-picker-wrapper input[type="color"] {
  border: none;
  width: 24px;
  height: 20px;
  cursor: pointer;
  background: none;
  padding: 0;
}

.flex-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.editor-controls-card {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}
</style>
