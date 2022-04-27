module TC_NorNorLatch (s, r, q, qn);
    input s;
    input r;
    output q;
    output qn;
    
    assign q = ~(r | qn);
    assign qn = ~(s | q);
endmodule
