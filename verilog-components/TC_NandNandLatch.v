module TC_NandNandLatch (s, r, q, qn);
    parameter UUID = 0;
    parameter NAME = "";
    input s;
    input r;
    output q;
    output qn;
    
    assign q = ~(s & q);
    assign qn = ~(r & qn);
endmodule

