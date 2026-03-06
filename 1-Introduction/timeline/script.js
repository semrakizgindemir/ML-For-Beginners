const timeline = document.getElementById("timeline");

events.forEach(ev => {
    const item = document.createElement("div");
    item.className = "timeline-item";

    item.innerHTML = `
    <div class="timeline-content">
      <div class="date">${ev.year}</div>
      <div class="title-text">${ev.title}</div>
      <div class="description">${ev.desc}</div>
      <img src="${ev.img}" class="thumbnail">
    </div>
  `;

    timeline.appendChild(item);
});
