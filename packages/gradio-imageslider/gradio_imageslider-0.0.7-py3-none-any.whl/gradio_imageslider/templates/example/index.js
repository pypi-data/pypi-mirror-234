const {
  SvelteComponent: g,
  attr: _,
  detach: m,
  element: d,
  init: o,
  insert: v,
  noop: r,
  safe_not_equal: y,
  src_url_equal: u,
  toggle_class: i
} = window.__gradio__svelte__internal;
function b(a) {
  let e, t;
  return {
    c() {
      e = d("img"), u(e.src, t = /*samples_dir*/
      a[1] + /*value*/
      a[0]) || _(e, "src", t), _(e, "class", "svelte-ljn2uo"), i(
        e,
        "table",
        /*type*/
        a[2] === "table"
      ), i(
        e,
        "gallery",
        /*type*/
        a[2] === "gallery"
      ), i(
        e,
        "selected",
        /*selected*/
        a[3]
      );
    },
    m(l, s) {
      v(l, e, s);
    },
    p(l, [s]) {
      s & /*samples_dir, value*/
      3 && !u(e.src, t = /*samples_dir*/
      l[1] + /*value*/
      l[0]) && _(e, "src", t), s & /*type*/
      4 && i(
        e,
        "table",
        /*type*/
        l[2] === "table"
      ), s & /*type*/
      4 && i(
        e,
        "gallery",
        /*type*/
        l[2] === "gallery"
      ), s & /*selected*/
      8 && i(
        e,
        "selected",
        /*selected*/
        l[3]
      );
    },
    i: r,
    o: r,
    d(l) {
      l && m(e);
    }
  };
}
function h(a, e, t) {
  let { value: l } = e, { samples_dir: s } = e, { type: c } = e, { selected: f = !1 } = e;
  return a.$$set = (n) => {
    "value" in n && t(0, l = n.value), "samples_dir" in n && t(1, s = n.samples_dir), "type" in n && t(2, c = n.type), "selected" in n && t(3, f = n.selected);
  }, [l, s, c, f];
}
class q extends g {
  constructor(e) {
    super(), o(this, e, h, b, y, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
export {
  q as default
};
