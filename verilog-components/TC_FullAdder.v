module TC_FullAdder (a, b, ci, out, co)
    input a;
    input b;
    input ci;
    output out;
    output co;
    
    assign out = a ^ b ^ ci;
    assign co = (a & b) | ((a ^ b) & ci);
endmodule

