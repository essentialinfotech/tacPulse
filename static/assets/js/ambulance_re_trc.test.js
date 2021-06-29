const rewire = require("rewire")
const ambulance_re_trc = rewire("./ambulance_re_trc")
const trackMap = ambulance_re_trc.__get__("trackMap")
    // @ponicode
describe("trackMap", () => {
    test("0", () => {
        let callFunction = () => {
            trackMap()
        }

        expect(callFunction).not.toThrow()
    })
})