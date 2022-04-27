module TC_Decoder3 (dis, sel0, sel1, sel2, out0, out1, out2, out3, out4, out5, out6, out7);
    input dis;
    input sel0;
    input sel1;
    input sel2;
    output reg out0;
    output reg out1;
    output reg out2;
    output reg out3;
    output reg out4;
    output reg out5;
    output reg out6;
    output reg out7;

    always @ (dis or {sel2, sel1, sel0})
    begin
        if(dis)
            out <= 8'b0000_0000;
        else begin
            case({sel2, sel1, sel0})
            3'b000 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0000_0001;
            3'b001 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0000_0010;
            3'b010 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0000_0100;
            3'b011 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0000_1000;
            3'b100 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0001_0000;
            3'b101 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0010_0000;
            3'b110 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b0100_0000;
            3'b111 : {out7, out6, out5, out4, out3, out2, out1, out0} <=  8'b1000_0000;
            endcase
        end
    end 
endmodule

