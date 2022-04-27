module TC_On(value);
    parameter size = 1;
    output value;
    
    assign value = {size{1'b1}};
endmodule

