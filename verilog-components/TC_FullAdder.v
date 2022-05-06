module TC_FullAdder (in0, in1, ci, out, co);
    parameter UUID = 0;
    parameter NAME = "";
    input in0;
    input in1;
    input ci;
    output out;
    output co;
    
    assign out = in0 ^ in1 ^ ci;
    assign co = (in0 & in1) | ((in0 ^ in1) & ci);
endmodule

