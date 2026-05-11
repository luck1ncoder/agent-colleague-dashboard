import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from tmpl_engine import render

class TestVarSubstitution(unittest.TestCase):
    def test_simple_var(self):
        self.assertEqual(render("hello {{name}}", {"name": "Cole"}), "hello Cole")

    def test_dot_path(self):
        data = {"user": {"name": "Cole", "tier": "S"}}
        self.assertEqual(render("{{user.name}} ({{user.tier}})", data), "Cole (S)")

    def test_missing_var_renders_empty(self):
        self.assertEqual(render("hello {{name}}", {}), "hello ")

    def test_multiple_vars_one_line(self):
        data = {"a": "1", "b": "2"}
        self.assertEqual(render("{{a}}-{{b}}", data), "1-2")

    def test_no_vars(self):
        self.assertEqual(render("plain text", {}), "plain text")

class TestEachLoop(unittest.TestCase):
    def test_each_simple(self):
        tmpl = "{{#each tags}}<span>{{this}}</span>{{/each}}"
        out = render(tmpl, {"tags": ["a", "b", "c"]})
        self.assertEqual(out, "<span>a</span><span>b</span><span>c</span>")

    def test_each_dict_items(self):
        tmpl = "{{#each items}}{{this.name}}={{this.val}};{{/each}}"
        out = render(tmpl, {"items": [{"name": "x", "val": "1"}, {"name": "y", "val": "2"}]})
        self.assertEqual(out, "x=1;y=2;")

    def test_each_empty_list(self):
        tmpl = "before{{#each items}}LOOP{{/each}}after"
        self.assertEqual(render(tmpl, {"items": []}), "beforeafter")

    def test_each_missing_key(self):
        tmpl = "before{{#each missing}}LOOP{{/each}}after"
        self.assertEqual(render(tmpl, {}), "beforeafter")

    def test_each_with_outer_var(self):
        tmpl = "{{title}}: {{#each items}}{{this}}, {{/each}}"
        self.assertEqual(render(tmpl, {"title": "list", "items": ["a", "b"]}), "list: a, b, ")

    def test_each_nested(self):
        tmpl = "{{#each groups}}[{{this.name}}:{{#each this.tags}}{{this}},{{/each}}]{{/each}}"
        data = {"groups": [
            {"name": "a", "tags": ["x", "y"]},
            {"name": "b", "tags": ["z"]},
        ]}
        self.assertEqual(render(tmpl, data), "[a:x,y,][b:z,]")

    def test_each_with_inner_if(self):
        tmpl = "{{#each items}}{{#if this.flag}}[{{this.name}}]{{/if}}{{/each}}"
        data = {"items": [
            {"name": "shown", "flag": True},
            {"name": "hidden", "flag": False},
            {"name": "also-shown", "flag": True},
        ]}
        self.assertEqual(render(tmpl, data), "[shown][also-shown]")


class TestIfCond(unittest.TestCase):
    def test_if_truthy(self):
        tmpl = "{{#if name}}Hello {{name}}{{/if}}"
        self.assertEqual(render(tmpl, {"name": "Cole"}), "Hello Cole")

    def test_if_falsy_missing(self):
        tmpl = "before{{#if name}}HIDDEN{{/if}}after"
        self.assertEqual(render(tmpl, {}), "beforeafter")

    def test_if_falsy_empty_string(self):
        tmpl = "before{{#if name}}HIDDEN{{/if}}after"
        self.assertEqual(render(tmpl, {"name": ""}), "beforeafter")

    def test_if_falsy_zero(self):
        tmpl = "{{#if count}}has{{/if}}"
        self.assertEqual(render(tmpl, {"count": 0}), "")

    def test_if_falsy_empty_list(self):
        tmpl = "{{#if tags}}has tags{{/if}}"
        self.assertEqual(render(tmpl, {"tags": []}), "")

if __name__ == "__main__":
    unittest.main()
