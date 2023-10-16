
export const TOOLBOX_JUNKBOX = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'CATEGORY',
      name: '%{BKY_TOOLBOX_JUNKBOX}',
      colour: 330,
      contents: [
        {
          kind: 'BLOCK',
          type: 'text_nocrlf_print',
          blockxml:
           `<block type='text_nocrlf_print'>
              <value name='TEXT'>
                <shadow type='text'>
                  <field name='TEXT'>abc</field>
                </shadow>
              </value>
            </block>`,
        },

        {
          kind: 'BLOCK',
          type: 'color_hsv2rgb',
          blockxml:
           `<block type='color_hsv2rgb'>
              <value name='H'>
                <shadow type='math_number'>
                  <field name='NUM'>0.0</field>
                </shadow>
              </value>
              <value name='S'>
                <shadow type='math_number'>
                  <field name='NUM'>0.45</field>
                </shadow>
              </value>
              <value name='V'>
                <shadow type='math_number'>
                  <field name='NUM'>0.65</field>
                </shadow>
              </value>
            </block>`,
        },

      ]
    }
  ]
};

