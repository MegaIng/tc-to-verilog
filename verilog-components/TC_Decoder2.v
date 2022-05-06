module TC_Decoder2 (sel0, sel1, out0, out1, out2, out3);
    parameter UUID = 0;
    parameter NAME = "";
    input sel0;
    input sel1;
    output reg out0;
    output reg out1;
    output reg out2;
    output reg out3;

    always @ (sel1, sel0) begin
        case({sel1, sel0})
        2'b00 : {out3, out2, out1, out0} =  4'b0001;
        2'b01 : {out3, out2, out1, out0} =  4'b0010;
        2'b10 : {out3, out2, out1, out0} =  4'b0100;
        2'b11 : {out3, out2, out1, out0} =  4'b1000;
        endcase
    end 
endmodule

