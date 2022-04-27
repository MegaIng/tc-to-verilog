module TC_SRLatch (s, r, q, qn);
    input s;
    input r;
    output q;
    output qn;
    
    assign q = ~(s & q);
    assign qn = ~(r & qn);
endmodule

