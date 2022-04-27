module TC_Decoder1 (sel, out0, out1);
    input sel;
    output reg out0, out1;

    always @ (sel)
    begin
        case(sel)
        1'b0 : {out1, out0} <=  2'b01;
        1'b1 : {out1, out0} <=  2'b10;
        endcase
    end 
endmodule

