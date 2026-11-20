async () => {
  const NAME = "__SHEET_NAME__";
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // Activate the tab so its cells are loaded into memory. Only the active
  // sheet's grid is resident; reading an inactive sheet returns blanks.
  const tabs = [...document.querySelectorAll('*')].filter(
    e => e.children.length === 0 && (e.textContent || '').trim() === NAME
  );
  if (tabs.length) {
    const el = tabs[0];
    const r = el.getBoundingClientRect();
    const o = { bubbles: true, cancelable: true, view: window, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2 };
    el.dispatchEvent(new MouseEvent('mousedown', o));
    el.dispatchEvent(new MouseEvent('mouseup', o));
    el.dispatchEvent(new MouseEvent('click', o));
    await sleep(2500);
  }

  const sheets = window.APP.workbook._worksheets._sheets;
  const s = sheets.find(x => { try { return x.getName() === NAME; } catch (e) { return false; } });
  if (!s) return JSON.stringify({ error: 'sheet not found: ' + NAME });

  const MAXC = 60, MAXR = 800;

  // Widest column that has content in the header or first data rows.
  let maxC = 0;
  for (let c = 0; c < MAXC; c++) {
    let any = false;
    for (let r = 0; r < 4; r++) {
      const v = s.getCellString(r, c);
      if (v && String(v).trim()) { any = true; break; }
    }
    if (any) maxC = c;
  }

  // Scan rows until 8 consecutive fully-empty rows.
  const rows = [];
  let blank = 0;
  for (let r = 0; r < MAXR; r++) {
    const row = [];
    let empty = true;
    for (let c = 0; c <= maxC; c++) {
      const v = s.getCellString(r, c);
      const t = v == null ? '' : String(v);
      row.push(t);
      if (t.trim()) empty = false;
    }
    if (empty) { blank++; if (blank >= 8) break; rows.push(row); }
    else { blank = 0; rows.push(row); }
  }

  return JSON.stringify({ name: NAME, header: rows[0] || [], rows });
}
