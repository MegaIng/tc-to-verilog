module TC_Off(value);
    parameter BIT_WIDTH = 1;
    output value;
    
    assign value = {BIT_WIDTH{1'b0}};
endmodule

