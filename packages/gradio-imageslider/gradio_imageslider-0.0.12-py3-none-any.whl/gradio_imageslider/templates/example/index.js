const {
  SvelteComponent: y,
  append: u,
  attr: _,
  detach: p,
  element: m,
  init: b,
  insert: k,
  noop: o,
  safe_not_equal: h,
  space: w,
  src_url_equal: d,
  toggle_class: f
} = window.__gradio__svelte__internal;
function q(l) {
  let e, s, n, g, i, c, t, v;
  return {
    c() {
      e = m("div"), s = m("img"), g = w(), i = m("img"), t = w(), v = m("span"), d(s.src, n = /*samples_dir*/
      l[1] + /*value*/
      l[0][0]) || _(s, "src", n), _(s, "class", "svelte-l4wpk0"), d(i.src, c = /*samples_dir*/
      l[1] + /*value*/
      l[0][1]) || _(i, "src", c), _(i, "class", "svelte-l4wpk0"), _(v, "class", "svelte-l4wpk0"), _(e, "class", "wrap svelte-l4wpk0"), f(
        e,
        "table",
        /*type*/
        l[2] === "table"
      ), f(
        e,
        "gallery",
        /*type*/
        l[2] === "gallery"
      ), f(
        e,
        "selected",
        /*selected*/
        l[3]
      );
    },
    m(a, r) {
      k(a, e, r), u(e, s), u(e, g), u(e, i), u(e, t), u(e, v);
    },
    p(a, [r]) {
      r & /*samples_dir, value*/
      3 && !d(s.src, n = /*samples_dir*/
      a[1] + /*value*/
      a[0][0]) && _(s, "src", n), r & /*samples_dir, value*/
      3 && !d(i.src, c = /*samples_dir*/
      a[1] + /*value*/
      a[0][1]) && _(i, "src", c), r & /*type*/
      4 && f(
        e,
        "table",
        /*type*/
        a[2] === "table"
      ), r & /*type*/
      4 && f(
        e,
        "gallery",
        /*type*/
        a[2] === "gallery"
      ), r & /*selected*/
      8 && f(
        e,
        "selected",
        /*selected*/
        a[3]
      );
    },
    i: o,
    o,
    d(a) {
      a && p(e);
    }
  };
}
function I(l, e, s) {
  let { value: n } = e, { samples_dir: g } = e, { type: i } = e, { selected: c = !1 } = e;
  return l.$$set = (t) => {
    "value" in t && s(0, n = t.value), "samples_dir" in t && s(1, g = t.samples_dir), "type" in t && s(2, i = t.type), "selected" in t && s(3, c = t.selected);
  }, l.$$.update = () => {
    l.$$.dirty & /*value, samples_dir*/
    3 && console.log(n, g);
  }, [n, g, i, c];
}
class C extends y {
  constructor(e) {
    super(), b(this, e, I, q, h, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
export {
  C as default
};
