const {
  SvelteComponent: o,
  attr: g,
  detach: r,
  element: c,
  init: v,
  insert: m,
  noop: d,
  safe_not_equal: b,
  space: y,
  src_url_equal: u,
  toggle_class: i
} = window.__gradio__svelte__internal;
function j(t) {
  let e, n, _, a, f;
  return {
    c() {
      e = c("img"), _ = y(), a = c("img"), u(e.src, n = /*samples_dir*/
      t[1] + /*value*/
      t[0][0]) || g(e, "src", n), g(e, "class", "svelte-ljn2uo"), i(
        e,
        "table",
        /*type*/
        t[2] === "table"
      ), i(
        e,
        "gallery",
        /*type*/
        t[2] === "gallery"
      ), i(
        e,
        "selected",
        /*selected*/
        t[3]
      ), u(a.src, f = /*samples_dir*/
      t[1] + /*value*/
      t[0][1]) || g(a, "src", f), g(a, "class", "svelte-ljn2uo"), i(
        a,
        "table",
        /*type*/
        t[2] === "table"
      ), i(
        a,
        "gallery",
        /*type*/
        t[2] === "gallery"
      ), i(
        a,
        "selected",
        /*selected*/
        t[3]
      );
    },
    m(s, l) {
      m(s, e, l), m(s, _, l), m(s, a, l);
    },
    p(s, [l]) {
      l & /*samples_dir, value*/
      3 && !u(e.src, n = /*samples_dir*/
      s[1] + /*value*/
      s[0][0]) && g(e, "src", n), l & /*type*/
      4 && i(
        e,
        "table",
        /*type*/
        s[2] === "table"
      ), l & /*type*/
      4 && i(
        e,
        "gallery",
        /*type*/
        s[2] === "gallery"
      ), l & /*selected*/
      8 && i(
        e,
        "selected",
        /*selected*/
        s[3]
      ), l & /*samples_dir, value*/
      3 && !u(a.src, f = /*samples_dir*/
      s[1] + /*value*/
      s[0][1]) && g(a, "src", f), l & /*type*/
      4 && i(
        a,
        "table",
        /*type*/
        s[2] === "table"
      ), l & /*type*/
      4 && i(
        a,
        "gallery",
        /*type*/
        s[2] === "gallery"
      ), l & /*selected*/
      8 && i(
        a,
        "selected",
        /*selected*/
        s[3]
      );
    },
    i: d,
    o: d,
    d(s) {
      s && (r(e), r(_), r(a));
    }
  };
}
function q(t, e, n) {
  let { value: _ } = e, { samples_dir: a } = e, { type: f } = e, { selected: s = !1 } = e;
  return t.$$set = (l) => {
    "value" in l && n(0, _ = l.value), "samples_dir" in l && n(1, a = l.samples_dir), "type" in l && n(2, f = l.type), "selected" in l && n(3, s = l.selected);
  }, t.$$.update = () => {
    t.$$.dirty & /*value, samples_dir*/
    3 && console.log(_, a);
  }, [_, a, f, s];
}
class w extends o {
  constructor(e) {
    super(), v(this, e, q, j, b, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
export {
  w as default
};
