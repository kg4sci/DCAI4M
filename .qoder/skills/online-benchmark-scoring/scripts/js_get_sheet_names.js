() => JSON.stringify(
  window.APP.workbook._worksheets._sheets.map(s => {
    try { return s.getName(); } catch (e) { return null; }
  })
)
