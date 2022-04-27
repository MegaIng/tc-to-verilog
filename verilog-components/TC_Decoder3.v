module TC_Decoder3 (dis, sel, out);
    input dis;
    input [2:0] sel;
    output reg [7:0] out;

    always @ (dis or sel)
    begin
        if(dis)
            out <= 8'b0000_0000;
        else begin
            case(sel)
            3'b000 : out <=  8'b0000_0001;
            3'b001 : out <=  8'b0000_0010;
            3'b010 : out <=  8'b0000_0100;
            3'b011 : out <=  8'b0000_1000;
            3'b100 : out <=  8'b0001_0000;
            3'b101 : out <=  8'b0010_0000;
            3'b110 : out <=  8'b0100_0000;
            3'b111 : out <=  8'b1000_0000;
            endcase
        end
    end 
endmodule

