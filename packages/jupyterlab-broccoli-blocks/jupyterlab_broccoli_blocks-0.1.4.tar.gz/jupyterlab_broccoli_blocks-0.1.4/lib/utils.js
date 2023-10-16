//
export class ToolboxUtils {
    constructor() { }
    add(a, b, num) {
        //
        if (a.kind !== b.kind)
            undefined;
        const c = { kind: a.kind, contents: new Array };
        const a_len = a.contents.length;
        const b_len = b.contents.length;
        for (let i = 0; i < a_len; i++) {
            c.contents[i] = a.contents[i];
        }
        // separator
        for (let i = 0; i < num; i++) {
            c.contents[a_len + i] = { kind: 'SEP' };
        }
        for (let i = 0; i < b_len; i++) {
            c.contents[a_len + num + i] = b.contents[i];
        }
        return c;
    }
}
//# sourceMappingURL=utils.js.map